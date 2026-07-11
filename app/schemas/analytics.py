from pydantic import BaseModel


class CategoryTotal(BaseModel):
    category_id: str
    category_name: str
    category_color: str
    total: float

class MonthlyEvolution(BaseModel):
    year: int
    month: int
    income: float
    expense: float

class AccountBalance(BaseModel):
    account_id: str
    account_name: str
    initial_balance: float
    current_balance: float