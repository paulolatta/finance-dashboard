from datetime import datetime, timezone
from enum import Enum

from beanie import Document, Indexed
from pydantic import Field
from typing_extensions import Annotated


class AccountType(str, Enum):
    CHECKING = "checking"
    SAVINGS = "savings"
    CREDIT_CARD = "credit_card"
    CASH = "cash"


class Account(Document):
    name: str
    type: AccountType
    initial_balance: float = 0.0
    user_id: Annotated[str, Indexed()]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "accounts"