from datetime import datetime

from fastapi import APIRouter, Query

from app.models.account import Account
from app.models.transaction import Transaction
from app.schemas.analytics import CategoryTotal, MonthlyEvolution, AccountBalance


router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/totals-by-category", response_model=list[CategoryTotal])
async def totals_by_category(
    start_date: datetime = Query(...),
    end_date: datetime = Query(...),
):
    pipeline = [
        {
            "$match": {
                "date": {"$gte": start_date, "$lte": end_date},
                "type": "expense",
            }
        },
        {
            "$group": {
                "_id": "$category.$id",
                "total": {"$sum": "$amount"},
            }
        },
        {
            "$lookup": {
                "from": "categories",
                "localField": "_id",
                "foreignField": "_id",
                "as": "category",
            }
        },
        {"$unwind": "$category"},
        {
            "$project": {
                "_id": 0,
                "category_id": {"$toString": "$_id"},
                "category_name": "$category.name",
                "category_color": "$category.color",
                "total": 1,
            }
        },
        {"$sort": {"total": -1}},
    ]

    results = await Transaction.get_motor_collection().aggregate(pipeline).to_list(None)
    return results


@router.get("/monthly-evolution", response_model=list[MonthlyEvolution])
async def monthly_evolution(
    start_date: datetime = Query(...),
    end_date: datetime = Query(...),
):
    pipeline = [
        {"$match": {"date": {"$gte": start_date, "$lte": end_date}}},
        {
            "$group": {
                "_id": {
                    "year": {"$year": "$date"},
                    "month": {"$month": "$date"},
                    "type": "$type",
                },
                "total": {"$sum": "$amount"},
            }
        },
        {
            "$group": {
                "_id": {"year": "$_id.year", "month": "$_id.month"},
                "amounts": {"$push": {"type": "$_id.type", "total": "$total"}},
            }
        },
        {
            "$project": {
                "_id": 0,
                "year": "$_id.year",
                "month": "$_id.month",
                "income": {
                    "$sum": {
                        "$map": {
                            "input": {
                                "$filter": {
                                    "input": "$amounts",
                                    "cond": {"$eq": ["$$this.type", "income"]},
                                }
                            },
                            "in": "$$this.total",
                        }
                    }
                },
                "expense": {
                    "$sum": {
                        "$map": {
                            "input": {
                                "$filter": {
                                    "input": "$amounts",
                                    "cond": {"$eq": ["$$this.type", "expense"]},
                                }
                            },
                            "in": "$$this.total",
                        }
                    }
                },
            }
        },
        {"$sort": {"year": 1, "month": 1}},
    ]

    results = await Transaction.get_motor_collection().aggregate(pipeline).to_list(None)
    return results

@router.get("/account-balances", response_model=list[AccountBalance])
async def account_balances():
    pipeline = [
        {
            "$group": {
                "_id": "$account.$id",
                "income": {
                    "$sum": {"$cond": [{"$eq": ["$type", "income"]}, "$amount", 0]}
                },
                "expense": {
                    "$sum": {"$cond": [{"$eq": ["$type", "expense"]}, "$amount", 0]}
                },
            }
        }
    ]

    totals_by_account = await Transaction.get_motor_collection().aggregate(pipeline).to_list(None)
    totals_map = {t["_id"]: t["income"] - t["expense"] for t in totals_by_account}

    accounts = await Account.find_all().to_list()

    return [
        AccountBalance(
            account_id=str(acc.id),
            account_name=acc.name,
            initial_balance=acc.initial_balance,
            current_balance=acc.initial_balance + totals_map.get(acc.id, 0),
        )
        for acc in accounts
    ]