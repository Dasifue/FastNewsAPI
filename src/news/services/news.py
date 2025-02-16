"""
Services module contains business logic
"""

import asyncio
from typing import Sequence

from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from ..models import News
from ..utils import save_media
from .categories import CategoryService

from src.manager import DBManager


class NewsService():

    @classmethod
    async def get_news(
        cls,
        db: AsyncSession,
        offset: int = 0,
        limit: int = 10,
    ) -> Sequence[News]:
        """
        Service
        """
        return await DBManager.get_objects(db, model=News, offset=offset, limit=limit)


    @classmethod
    async def get_news_object(
        cls,
        db: AsyncSession,
        news_id: int,
    ) -> News:
        """
        Service
        """
        news = await DBManager.get_object(db=db, model=News, field="id", value=news_id, option=joinedload(News.category))
        if news is None:
            raise HTTPException(status_code=404, detail="News not found")
        return news


    @classmethod
    async def create_news(
        cls,
        db: AsyncSession,
        news: dict
    ) -> News:
        """
        Service
        """

        await CategoryService.get_category(db, category_id=news["category_id"])

        news["images"] = await asyncio.gather(*[save_media(file) for file in news["images"]])

        return await DBManager.create_object(**news, db=db, model=News, commit=True)


    @classmethod
    async def delete_news(
        cls,
        db: AsyncSession,
        news_id: int
    ) -> None:
        """
        Service
        """
        await DBManager.delete_object(db=db, model=News, field="id", value=news_id, commit=True)


    @classmethod
    async def update_news(
        cls,
        db: AsyncSession,
        news_id: int,
        news: dict,
    ) -> News:
        """
        Service
        """

        await CategoryService.get_category(db=db, category_id=news["category_id"])

        news["images"] = await asyncio.gather(*[save_media(file) for file in news["images"]])

        news = await DBManager.update_object(**news, db=db, model=News, field="id", value=news_id, commit=True)

        if news is None:
            raise HTTPException(status_code=404, detail="News not found")
        return news


    @classmethod
    async def partial_update_news(
        cls,
        db: AsyncSession,
        news_id: int,
        news: dict,
    ) -> News:
        """
        Service
        """

        if news["category_id"]:
            await CategoryService.get_category(db=db, category_id=news["category_id"])

        if news["images"]:
            news["images"] = await asyncio.gather(*[save_media(file) for file in news["images"]])

        news = await DBManager.partial_update_object(**news, db=db, model=News, field="id", value=news_id, commit=True)

        if news is None:
            raise HTTPException(status_code=404, detail="News not found")
        return news
