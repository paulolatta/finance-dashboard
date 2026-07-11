from enum import Enum

from beanie import Document


class CategoryType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"


class Category(Document):
    name: str
    type: CategoryType
    color: str = "#6B7280"
    icon: str | None = None

    class Settings:
        name = "categories"