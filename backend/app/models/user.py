from datetime import datetime, timezone

from beanie import Document, Indexed
from pydantic import Field
from typing_extensions import Annotated


class User(Document):
    email: Annotated[str, Indexed(unique=True)]
    hashed_password: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "users"