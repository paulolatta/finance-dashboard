from fastapi import APIRouter, HTTPException, Query, status

from app.models.account import Account
from app.models.category import Category
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionRead, TransactionUpdate

import io

import pandas as pd
from fastapi import File, UploadFile

from app.services.categorization import suggest_category
from app.schemas.import_transactions import (
    ImportPreviewItem,
    ImportConfirmRequest,
    ImportConfirmItem,
)

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
):
    transactions = (
        await Transaction.find_all()
        .sort(-Transaction.date)
        .skip(skip)
        .limit(limit)
        .to_list()
    )
    return [to_read(t) for t in transactions]


@router.get("/{transaction_id}", response_model=TransactionRead)
async def get_transaction(transaction_id: str):
    transaction = await Transaction.get(transaction_id)
    if transaction is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    return to_read(transaction)


@router.post("/", response_model=TransactionRead, status_code=status.HTTP_201_CREATED)
async def create_transaction(payload: TransactionCreate):
    account = await Account.get(payload.account_id)
    if account is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")

    category = await Category.get(payload.category_id)
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    transaction = Transaction(
        description=payload.description,
        amount=payload.amount,
        date=payload.date,
        type=payload.type,
        account=account,
        category=category,
        tags=payload.tags,
    )
    await transaction.insert()
    return to_read(transaction)


@router.patch("/{transaction_id}", response_model=TransactionRead)
async def update_transaction(transaction_id: str, payload: TransactionUpdate):
    transaction = await Transaction.get(transaction_id)
    if transaction is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")

    update_data = payload.model_dump(exclude_unset=True, exclude={"account_id", "category_id"})
    for field, value in update_data.items():
        setattr(transaction, field, value)

    if payload.account_id is not None:
        account = await Account.get(payload.account_id)
        if account is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
        transaction.account = account

    if payload.category_id is not None:
        category = await Category.get(payload.category_id)
        if category is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        transaction.category = category

    await transaction.save()
    return to_read(transaction)


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(transaction_id: str):
    transaction = await Transaction.get(transaction_id)
    if transaction is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    await transaction.delete()

@router.post("/import/preview", response_model=list[ImportPreviewItem])
async def preview_import(file: UploadFile = File(...)):
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
        category = await suggest_category(str(row["description"]))

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
async def confirm_import(payload: ImportConfirmRequest):
    created_transactions = []

    for item in payload.items:
        account = await Account.get(item.account_id)
        if account is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Account not found: {item.account_id}",
            )

        category = await Category.get(item.category_id)
        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category not found: {item.category_id}",
            )

        transaction = Transaction(
            description=item.description,
            amount=item.amount,
            date=item.date,
            type=item.type,
            account=account,
            category=category,
        )
        await transaction.insert()
        created_transactions.append(transaction)

    return [to_read(t) for t in created_transactions]