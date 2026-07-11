from datetime import datetime

from pydantic import BaseModel

from app.models.account import AccountType


class AccountCreate(BaseModel):
    name: str
    type: AccountType
    initial_balance: float = 0.0


class AccountUpdate(BaseModel):
    name: str | None = None
    type: AccountType | None = None
    initial_balance: float | None = None


class AccountRead(BaseModel):
    id: str
    name: str
    type: AccountType
    initial_balance: float
    created_at: datetime

    class Config:
        from_attributes = True