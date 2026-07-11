import asyncio
from datetime import datetime, timedelta, timezone

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app.core.config import settings
from app.models import Account, AccountType, Category, CategoryType, Transaction, TransactionType


async def seed():
    client = AsyncIOMotorClient(settings.mongodb_uri)
    database = client[settings.mongodb_db_name]
    await init_beanie(database=database, document_models=[Account, Category, Transaction])

    # Limpa dados existentes antes de popular de novo
    await Account.delete_all()
    await Category.delete_all()
    await Transaction.delete_all()

    # --- Accounts ---
    checking = Account(name="Conta Corrente", type=AccountType.CHECKING, initial_balance=1500.0)
    savings = Account(name="Poupança", type=AccountType.SAVINGS, initial_balance=5000.0)
    credit_card = Account(name="Cartão Nubank", type=AccountType.CREDIT_CARD, initial_balance=0.0)
    await checking.insert()
    await savings.insert()
    await credit_card.insert()

    # --- Categories ---
    salary = Category(name="Salário", type=CategoryType.INCOME, color="#22C55E")
    freelance = Category(name="Freelance", type=CategoryType.INCOME, color="#16A34A")
    food = Category(name="Alimentação", type=CategoryType.EXPENSE, color="#EF4444")
    transport = Category(name="Transporte", type=CategoryType.EXPENSE, color="#F97316")
    leisure = Category(name="Lazer", type=CategoryType.EXPENSE, color="#8B5CF6")
    subscriptions = Category(name="Assinaturas", type=CategoryType.EXPENSE, color="#3B82F6")

    for cat in [salary, freelance, food, transport, leisure, subscriptions]:
        await cat.insert()

    # --- Transactions (últimos 3 meses, dados variados) ---
    now = datetime.now(timezone.utc)
    transactions_data = [
        # Receitas mensais
        *[
            (salary, checking, TransactionType.INCOME, 5000.0, "Salário mensal", now - timedelta(days=30 * i))
            for i in range(3)
        ],
        (freelance, checking, TransactionType.INCOME, 1200.0, "Projeto freelance", now - timedelta(days=15)),

        # Despesas recorrentes e variadas
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
        )
        await transaction.insert()

    print(f"Seed completed:")
    print(f"  - {await Account.count()} accounts")
    print(f"  - {await Category.count()} categories")
    print(f"  - {await Transaction.count()} transactions")


if __name__ == "__main__":
    asyncio.run(seed())