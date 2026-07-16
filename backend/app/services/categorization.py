from app.models.category import Category

KEYWORD_RULES: dict[str, str] = {
    "supermercado": "Alimentação",
    "mercado": "Alimentação",
    "restaurante": "Alimentação",
    "ifood": "Alimentação",
    "delivery": "Alimentação",
    "uber": "Transporte",
    "combustível": "Transporte",
    "combustivel": "Transporte",
    "posto": "Transporte",
    "cinema": "Lazer",
    "netflix": "Assinaturas",
    "spotify": "Assinaturas",
    "salário": "Salário",
    "salario": "Salário",
    "freelance": "Freelance",
}


async def suggest_category(description: str, user_id: str) -> Category | None:
    description_lower = description.lower()

    matched_category_name = None
    for keyword, category_name in KEYWORD_RULES.items():
        if keyword in description_lower:
            matched_category_name = category_name
            break

    if matched_category_name is None:
        return None

    return await Category.find_one(
        Category.name == matched_category_name, Category.user_id == user_id
    )