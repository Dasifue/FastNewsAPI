"""
News Router
"""

from typing import Sequence, Annotated

from fastapi import APIRouter, Depends, Form, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db

from ..services import NewsService
from ..schemas import NewsReadSchema
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


@router.post("", response_model=NewsReadSchema)
async def get_news_object(
    title: Annotated[str, Form()],
    images: Annotated[list[UploadFile], File()],
    category_id: Annotated[int, Form()],
    content: Annotated[str | None, Form()] = None,
    db: AsyncSession = Depends(get_db),
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