from datetime import datetime, timezone
from enum import Enum

from beanie import Document, Link
from pydantic import Field

from app.models.account import Account
from app.models.category import Category


class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"


class Transaction(Document):
    description: str
    amount: float
    date: datetime
    type: TransactionType
    account: Link[Account]
    category: Link[Category]
    tags: list[str] = []
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "transactions"
        indexes = [
            [("account", 1), ("date", -1)],
            [("category", 1), ("date", -1)],
        ]