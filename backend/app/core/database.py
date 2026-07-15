from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app.core.config import settings
from app.models import Account, Category, Transaction, User

DOCUMENT_MODELS = [Account, Category, Transaction, User]


async def init_db() -> None:
    client = AsyncIOMotorClient(settings.mongodb_uri)
    database = client[settings.mongodb_db_name]

    await init_beanie(database=database, document_models=DOCUMENT_MODELS)