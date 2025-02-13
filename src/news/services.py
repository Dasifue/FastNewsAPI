"""
Services module contains business logic
"""

from typing import Sequence

from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from .models import Category

from src.manager import DBManager


class CategoryService():

    @classmethod
    async def get_categories(
        cls,
        db: AsyncSession,
        offset: int = 0,
        limit: int = 10,
    ) -> Sequence[Category]:
        """
        Service
        """
        return await DBManager.get_objects(db, model=Category, offset=offset, limit=limit)


    @classmethod
    async def get_category(
        cls,
        db: AsyncSession,
        category_id: int,

    ) -> Category:
        """
        Service
        """
        category = await DBManager.get_object(db=db, model=Category, field="id", value=category_id)
        if category is None:
            raise HTTPException(status_code=404, detail="Category not found")
        return category


    @classmethod
    async def create_category(
        cls,
        db: AsyncSession,
        category: dict
    ) -> Category:
        """
        Service
        """
        return await DBManager.create_object(**category, db=db, model=Category, commit=True)


    @classmethod
    async def delete_category(
        cls,
        db: AsyncSession,
        category_id: int
    ) -> None:
        """
        Service
        """
        await DBManager.delete_object(db=db, model=Category, field="id", value=category_id, commit=True)


    @classmethod
    async def update_category(
        cls,
        db: AsyncSession,
        category_id: int,
        category: dict,
        partial: bool = False
    ) -> Category:
        """
        Service
        """
        if partial:
            category = await DBManager.partial_update_object(**category, db=db, model=Category, field="id", value=category_id, commit=True)
        else:
            category = await DBManager.update_object(**category, db=db, model=Category, field="id", value=category_id, commit=True)

        if category is None:
            raise HTTPException(status_code=404, detail="Category not found")
        return category
