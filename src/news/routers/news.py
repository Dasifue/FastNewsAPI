"""
News Router
"""

from typing import Sequence, Annotated

from fastapi import APIRouter, Depends, Form, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db

from ..services import NewsService
from ..schemas import NewsReadSchema, NewsReadDetailsSchema
from ..models import News

router = APIRouter(
    prefix="/news",
    tags=["News"]
)


@router.get("", response_model=Sequence[NewsReadSchema])
async def get_news(offset: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)) -> Sequence[News]:
    """
    Get all news
    """
    return await NewsService.get_news(db=db, offset=offset, limit=limit)


@router.get("/{news_id}", response_model=NewsReadDetailsSchema)
async def get_news_object(news_id: int, db: AsyncSession = Depends(get_db)) -> News:
    """
    Get news by id
    """
    return await NewsService.get_news_object(db=db, news_id=news_id)


@router.post("", response_model=NewsReadSchema)
async def create_news_object(
    title:          Annotated[str, Form()],
    images:         Annotated[list[UploadFile], File()],
    category_id:    Annotated[int, Form()],
    content:        Annotated[str | None, Form()] = None,
    db:             AsyncSession = Depends(get_db),
) -> News:
    "Creates a news object"
    return await NewsService.create_news(
        db=db,
        news={
            "title": title,
            "content": content,
            "images": images,
            "category_id": category_id
        }
    )


@router.put("/{news_id}", response_model=NewsReadSchema)
async def update_news(
    news_id:        int,
    title:          Annotated[str, Form()],
    images:         Annotated[list[UploadFile], File()],
    category_id:    Annotated[int, Form()],
    content:        Annotated[str, Form()],
    db:             AsyncSession = Depends(get_db),
) -> News:
    """
    Updates a news object by id
    """
    return await NewsService.update_news(
        db=db,
        news_id=news_id,
        news={
            "title": title,
            "images": images,
            "category_id": category_id,
            "content": content
        }
    )


@router.patch("/{news_id}", response_model=NewsReadSchema)
async def partial_update_news(
    news_id:        int,
    title:          Annotated[str | None, Form()] = None,
    images:         Annotated[list[UploadFile], File()] = [],
    category_id:    Annotated[int | None, Form()] = None,
    content:        Annotated[str | None, Form()] = None,
    db:             AsyncSession = Depends(get_db),
) -> News:
    """
    Partially updates a news object by id
    """
    return await NewsService.partial_update_news(
        db=db,
        news_id=news_id,
        news={
            "title": title,
            "images": images,
            "category_id": category_id,
            "content": content
        }
    )

@router.delete("/{news_id}", status_code=204)
async def delete_news_object(news_id: int, db: AsyncSession = Depends(get_db)) -> None:
    """
    Deletes a news object by id
    """
    return await NewsService.delete_news(db=db, news_id=news_id)
