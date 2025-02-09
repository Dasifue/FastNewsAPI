"""
Routers for news app
"""

from typing import Sequence

from fastapi import APIRouter, HTTPException, Response

from .models import Category
from .schemas import CategoryReadSchema, CategoryCreateSchema

from src.manager import DBManager

category_router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


@category_router.get("", response_model=Sequence[CategoryReadSchema])
async def get_categories(offset: int = 0, limit: int = 10) -> Sequence[Category]:
    """
    Get all categories
    """
    return await DBManager.get_objects(model=Category, offset=offset, limit=limit)


@category_router.get("/{category_id}", response_model=CategoryReadSchema)
async def get_category(category_id: int) -> Category:
    """
    Get category by id
    """
    category = await DBManager.get_object(model=Category, object_id=category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@category_router.post("", response_model=CategoryReadSchema)
async def create_category(category: CategoryCreateSchema) -> Category:
    """
    Create category
    """
    new_category = Category(**category.dict())
    return await DBManager.create_object(instance=new_category)


@category_router.delete("/{category_id}")
async def delete_category(category_id: int) -> None:
    """
    Delete category by id
    """
    return await DBManager.delete_object(model=Category, object_id=category_id)


@category_router.put("/{category_id}", response_model=CategoryReadSchema)
async def update_category(category_id: int, category: CategoryCreateSchema) -> Category:
    """
    Update category by id
    """
    return await DBManager.update_object(model=Category, object_id=category_id, updated_data=category)



@category_router.patch("/{category_id}", response_model=CategoryReadSchema)
async def partial_update_category(category_id: int, category: CategoryCreateSchema) -> Category:
    """
    Update category by id
    """
    return await DBManager.partial_update_object(model=Category, object_id=category_id, updated_data=category)
