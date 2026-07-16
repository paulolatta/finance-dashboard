from fastapi import APIRouter, Depends, HTTPException, status

from app.core.deps import get_current_user
from app.models.category import Category
from app.models.user import User
from app.schemas.category import CategoryCreate, CategoryRead, CategoryUpdate

router = APIRouter(prefix="/categories", tags=["categories"])


def to_read(category: Category) -> CategoryRead:
    return CategoryRead(
        id=str(category.id),
        name=category.name,
        type=category.type,
        color=category.color,
        icon=category.icon,
    )


@router.get("/", response_model=list[CategoryRead])
async def list_categories(current_user: User = Depends(get_current_user)):
    categories = await Category.find(Category.user_id == str(current_user.id)).to_list()
    return [to_read(c) for c in categories]


@router.get("/{category_id}", response_model=CategoryRead)
async def get_category(category_id: str, current_user: User = Depends(get_current_user)):
    category = await Category.get(category_id)
    if category is None or category.user_id != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return to_read(category)


@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
async def create_category(payload: CategoryCreate, current_user: User = Depends(get_current_user)):
    category = Category(**payload.model_dump(), user_id=str(current_user.id))
    await category.insert()
    return to_read(category)


@router.patch("/{category_id}", response_model=CategoryRead)
async def update_category(
    category_id: str,
    payload: CategoryUpdate,
    current_user: User = Depends(get_current_user),
):
    category = await Category.get(category_id)
    if category is None or category.user_id != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(category, field, value)

    await category.save()
    return to_read(category)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_id: str, current_user: User = Depends(get_current_user)):
    category = await Category.get(category_id)
    if category is None or category.user_id != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    await category.delete()