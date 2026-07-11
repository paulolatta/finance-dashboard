from datetime import datetime

from pydantic import BaseModel

from app.models.transaction import TransactionType


class ImportPreviewItem(BaseModel):
    row_index: int
    date: datetime
    description: str
    amount: float
    type: TransactionType
    suggested_category_id: str | None
    suggested_category_name: str | None


class ImportConfirmItem(BaseModel):
    date: datetime
    description: str
    amount: float
    type: TransactionType
    account_id: str
    category_id: str


class ImportConfirmRequest(BaseModel):
    items: list[ImportConfirmItem]