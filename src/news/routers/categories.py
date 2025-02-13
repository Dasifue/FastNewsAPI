"""
Categories Router
"""


from typing import Sequence

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Category
from ..schemas import CategoryReadSchema, CategoryCreateSchema
from ..services import CategoryService

from src.database import get_db

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


@router.get("", response_model=Sequence[CategoryReadSchema])
async def get_categories(offset: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)) -> Sequence[Category]:
    """
    Get all categories
    """
    return await CategoryService.get_categories(db, offset, limit)


@router.get("/{category_id}", response_model=CategoryReadSchema)
async def get_category(category_id: int, db: AsyncSession = Depends(get_db)) -> Category:
    """
    Get category by id
    """
    return await CategoryService.get_category(db, category_id)


@router.post("", response_model=CategoryReadSchema)
async def create_category(category: CategoryCreateSchema, db: AsyncSession = Depends(get_db)) -> Category:
    """
    Create category
    """
    return await CategoryService.create_category(db, category.dict())


@router.delete("/{category_id}", status_code=204)
async def delete_category(category_id: int, db: AsyncSession = Depends(get_db)) -> None:
    """
    Delete category by id
    """
    return await CategoryService.delete_category(db, category_id)


@router.put("/{category_id}", response_model=CategoryReadSchema)
async def update_category(category_id: int, category: CategoryCreateSchema, db: AsyncSession = Depends(get_db)) -> Category:
    """
    Update category by id
    """
    return await CategoryService.update_category(db, category_id, category.dict())



@router.patch("/{category_id}", response_model=CategoryReadSchema)
async def partial_update_category(category_id: int, category: CategoryCreateSchema, db: AsyncSession = Depends(get_db)) -> Category:
    """
    Update category by id
    """
    return await CategoryService.update_category(db, category_id, category.dict(), partial=True)
