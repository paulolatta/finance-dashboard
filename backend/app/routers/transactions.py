import io
from datetime import datetime

import pandas as pd
from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status

from app.core.deps import get_current_user
from app.models.account import Account
from app.models.category import Category
from app.models.transaction import Transaction
from app.models.user import User
from app.schemas.transaction import TransactionCreate, TransactionRead, TransactionUpdate
from app.schemas.import_transactions import (
    ImportConfirmItem,
    ImportConfirmRequest,
    ImportPreviewItem,
)
from app.services.categorization import suggest_category

router = APIRouter(prefix="/transactions", tags=["transactions"])


def to_read(transaction: Transaction) -> TransactionRead:
    return TransactionRead(
        id=str(transaction.id),
        description=transaction.description,
        amount=transaction.amount,
        date=transaction.date,
        type=transaction.type,
        account_id=str(transaction.account.ref.id),
        category_id=str(transaction.category.ref.id),
        tags=transaction.tags,
        created_at=transaction.created_at,
    )


@router.get("/", response_model=list[TransactionRead])
async def list_transactions(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    start_date: datetime | None = Query(None),
    end_date: datetime | None = Query(None),
    account_id: str | None = Query(None),
    category_id: str | None = Query(None),
    current_user: User = Depends(get_current_user),
):
    query_filters: dict = {"user_id": str(current_user.id)}

    if start_date or end_date:
        date_filter = {}
        if start_date:
            date_filter["$gte"] = start_date
        if end_date:
            date_filter["$lte"] = end_date
        query_filters["date"] = date_filter

    if account_id:
        query_filters["account.$id"] = PydanticObjectId(account_id)

    if category_id:
        query_filters["category.$id"] = PydanticObjectId(category_id)

    transactions = (
        await Transaction.find(query_filters)
        .sort(-Transaction.date)
        .skip(skip)
        .limit(limit)
        .to_list()
    )
    return [to_read(t) for t in transactions]


@router.get("/{transaction_id}", response_model=TransactionRead)
async def get_transaction(transaction_id: str, current_user: User = Depends(get_current_user)):
    transaction = await Transaction.get(transaction_id)
    if transaction is None or transaction.user_id != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    return to_read(transaction)


async def _get_owned_account(account_id: str, user_id: str) -> Account:
    account = await Account.get(account_id)
    if account is None or account.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    return account


async def _get_owned_category(category_id: str, user_id: str) -> Category:
    category = await Category.get(category_id)
    if category is None or category.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category


@router.post("/", response_model=TransactionRead, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    payload: TransactionCreate, current_user: User = Depends(get_current_user)
):
    account = await _get_owned_account(payload.account_id, str(current_user.id))
    category = await _get_owned_category(payload.category_id, str(current_user.id))

    transaction = Transaction(
        description=payload.description,
        amount=payload.amount,
        date=payload.date,
        type=payload.type,
        account=account,
        category=category,
        tags=payload.tags,
        user_id=str(current_user.id),
    )
    await transaction.insert()
    return to_read(transaction)


@router.patch("/{transaction_id}", response_model=TransactionRead)
async def update_transaction(
    transaction_id: str,
    payload: TransactionUpdate,
    current_user: User = Depends(get_current_user),
):
    transaction = await Transaction.get(transaction_id)
    if transaction is None or transaction.user_id != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")

    update_data = payload.model_dump(exclude_unset=True, exclude={"account_id", "category_id"})
    for field, value in update_data.items():
        setattr(transaction, field, value)

    if payload.account_id is not None:
        transaction.account = await _get_owned_account(payload.account_id, str(current_user.id))

    if payload.category_id is not None:
        transaction.category = await _get_owned_category(payload.category_id, str(current_user.id))

    await transaction.save()
    return to_read(transaction)


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(transaction_id: str, current_user: User = Depends(get_current_user)):
    transaction = await Transaction.get(transaction_id)
    if transaction is None or transaction.user_id != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    await transaction.delete()


@router.post("/import/preview", response_model=list[ImportPreviewItem])
async def preview_import(
    file: UploadFile = File(...), current_user: User = Depends(get_current_user)
):
    content = await file.read()
    df = pd.read_csv(io.BytesIO(content))

    required_columns = {"date", "description", "amount", "type"}
    if not required_columns.issubset(df.columns):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"CSV must contain columns: {', '.join(required_columns)}",
        )

    preview_items = []
    for idx, row in df.iterrows():
        # Sugestão de categoria já restrita às categorias do próprio usuário
        category = await suggest_category(str(row["description"]), user_id=str(current_user.id))

        preview_items.append(
            ImportPreviewItem(
                row_index=idx,
                date=row["date"],
                description=row["description"],
                amount=float(row["amount"]),
                type=row["type"],
                suggested_category_id=str(category.id) if category else None,
                suggested_category_name=category.name if category else None,
            )
        )

    return preview_items


@router.post("/import/confirm", response_model=list[TransactionRead])
async def confirm_import(
    payload: ImportConfirmRequest, current_user: User = Depends(get_current_user)
):
    created_transactions = []

    for item in payload.items:
        account = await _get_owned_account(item.account_id, str(current_user.id))
        category = await _get_owned_category(item.category_id, str(current_user.id))

        transaction = Transaction(
            description=item.description,
            amount=item.amount,
            date=item.date,
            type=item.type,
            account=account,
            category=category,
            user_id=str(current_user.id),
        )
        await transaction.insert()
        created_transactions.append(transaction)

    return [to_read(t) for t in created_transactions]