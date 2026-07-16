import asyncio
from datetime import datetime, timedelta, timezone

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app.core.config import settings
from app.models import Account, AccountType, Category, CategoryType, Transaction, TransactionType, User
from app.services.security import hash_password

SEED_USER_EMAIL = "seed@example.com"
SEED_USER_PASSWORD = "seedpassword123"


async def seed():
    client = AsyncIOMotorClient(settings.mongodb_uri)
    database = client[settings.mongodb_db_name]
    await init_beanie(
        database=database, document_models=[Account, Category, Transaction, User]
    )

    # Limpa dados existentes antes de popular de novo
    await Account.delete_all()
    await Category.delete_all()
    await Transaction.delete_all()
    await User.delete_all()

    # --- User de teste ---
    seed_user = User(
        email=SEED_USER_EMAIL,
        hashed_password=hash_password(SEED_USER_PASSWORD),
    )
    await seed_user.insert()
    user_id = str(seed_user.id)

    print(f"Seed user created: {SEED_USER_EMAIL} / {SEED_USER_PASSWORD}")

    # --- Accounts ---
    checking = Account(name="Conta Corrente", type=AccountType.CHECKING, initial_balance=1500.0, user_id=user_id)
    savings = Account(name="Poupança", type=AccountType.SAVINGS, initial_balance=5000.0, user_id=user_id)
    credit_card = Account(name="Cartão Nubank", type=AccountType.CREDIT_CARD, initial_balance=0.0, user_id=user_id)
    await checking.insert()
    await savings.insert()
    await credit_card.insert()

    # --- Categories ---
    salary = Category(name="Salário", type=CategoryType.INCOME, color="#22C55E", user_id=user_id)
    freelance = Category(name="Freelance", type=CategoryType.INCOME, color="#16A34A", user_id=user_id)
    food = Category(name="Alimentação", type=CategoryType.EXPENSE, color="#EF4444", user_id=user_id)
    transport = Category(name="Transporte", type=CategoryType.EXPENSE, color="#F97316", user_id=user_id)
    leisure = Category(name="Lazer", type=CategoryType.EXPENSE, color="#8B5CF6", user_id=user_id)
    subscriptions = Category(name="Assinaturas", type=CategoryType.EXPENSE, color="#3B82F6", user_id=user_id)

    for cat in [salary, freelance, food, transport, leisure, subscriptions]:
        await cat.insert()

    # --- Transactions ---
    now = datetime.now(timezone.utc)
    transactions_data = [
        *[
            (salary, checking, TransactionType.INCOME, 5000.0, "Salário mensal", now - timedelta(days=30 * i))
            for i in range(3)
        ],
        (freelance, checking, TransactionType.INCOME, 1200.0, "Projeto freelance", now - timedelta(days=15)),
        (food, credit_card, TransactionType.EXPENSE, 450.0, "Supermercado", now - timedelta(days=5)),
        (food, credit_card, TransactionType.EXPENSE, 89.90, "Restaurante", now - timedelta(days=3)),
        (food, checking, TransactionType.EXPENSE, 120.0, "Delivery", now - timedelta(days=10)),
        (transport, credit_card, TransactionType.EXPENSE, 60.0, "Uber", now - timedelta(days=2)),
        (transport, checking, TransactionType.EXPENSE, 200.0, "Combustível", now - timedelta(days=20)),
        (leisure, credit_card, TransactionType.EXPENSE, 150.0, "Cinema e jantar", now - timedelta(days=8)),
        (subscriptions, credit_card, TransactionType.EXPENSE, 55.90, "Streaming", now - timedelta(days=1)),
        (subscriptions, credit_card, TransactionType.EXPENSE, 29.90, "Spotify", now - timedelta(days=1)),
        (food, credit_card, TransactionType.EXPENSE, 380.0, "Supermercado", now - timedelta(days=35)),
        (transport, checking, TransactionType.EXPENSE, 180.0, "Combustível", now - timedelta(days=50)),
        (leisure, credit_card, TransactionType.EXPENSE, 90.0, "Boliche", now - timedelta(days=45)),
    ]

    for category, account, t_type, amount, description, date in transactions_data:
        transaction = Transaction(
            description=description,
            amount=amount,
            date=date,
            type=t_type,
            account=account,
            category=category,
            user_id=user_id,
        )
        await transaction.insert()

    print(f"Seed completed:")
    print(f"  - {await Account.count()} accounts")
    print(f"  - {await Category.count()} categories")
    print(f"  - {await Transaction.count()} transactions")


if __name__ == "__main__":
    asyncio.run(seed())