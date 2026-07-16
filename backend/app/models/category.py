from enum import Enum

from beanie import Document, Indexed
from typing_extensions import Annotated


class CategoryType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"


class Category(Document):
    name: str
    type: CategoryType
    color: str = "#6B7280"
    icon: str | None = None
    user_id: Annotated[str, Indexed()]

    class Settings:
        name = "categories"