"""
Services module contains business logic
"""

import asyncio
from typing import Sequence

import aiofiles

from fastapi import HTTPException, UploadFile

from sqlalchemy.ext.asyncio import AsyncSession

from ..models import News
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
        news = await DBManager.get_object(db=db, model=News, field="id", value=news_id)
        if news is None:
            raise HTTPException(status_code=404, detail="news not found")
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

        category = await CategoryService.get_category(db, category_id=news["category_id"])
        if category is None:
            raise HTTPException(status_code=404, detail="Category not found")


        news["images"] = await asyncio.gather(*[save(file) for file in news["images"]])

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
        partial: bool = False
    ) -> News:
        """
        Service
        """
        if partial:
            news = await DBManager.partial_update_object(**news, db=db, model=News, field="id", value=news_id, commit=True)
        else:
            news = await DBManager.update_object(**news, db=db, model=News, field="id", value=news_id, commit=True)

        if news is None:
            raise HTTPException(status_code=404, detail="News not found")
        return news


async def save(upload_file: UploadFile) -> str:
    file_path = f"media/news/{upload_file.filename}"

    async with aiofiles.open(file=file_path, mode="wb") as file:
        await file.write(await upload_file.read())

    return file_path
