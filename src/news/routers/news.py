"""
News Router
"""

from typing import Sequence, Annotated

from fastapi import APIRouter, Depends, Form, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.redis import cache
from src.users import fastapi_users, User

from ..services import NewsService
from ..schemas import NewsReadSchema, NewsReadDetailsSchema
from ..models import News

router = APIRouter(
    prefix="/news",
    tags=["News"]
)

admin_user = fastapi_users.current_user(active=True, superuser=True)

@router.get("", response_model=Sequence[NewsReadSchema])
@cache(60 * 5)
async def get_news(offset: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)) -> Sequence[News]:
    """
    Get all news \n
    No authentication required \n
    """
    return await NewsService.get_news(db=db, offset=offset, limit=limit)


@router.get("/{news_id}", response_model=NewsReadDetailsSchema)
@cache(60 * 5)
async def get_news_object(news_id: int, db: AsyncSession = Depends(get_db)) -> News:
    """
    Get news by id \n
    No authentication required \n
    """
    return await NewsService.get_news_object(db=db, news_id=news_id)


@router.post("", response_model=NewsReadSchema)
async def create_news_object(
    title:          Annotated[str, Form()],
    images:         Annotated[list[UploadFile], File()],
    category_id:    Annotated[int, Form()],
    content:        Annotated[str | None, Form()] = None,
    db:             AsyncSession = Depends(get_db),
    user:           User = Depends(admin_user),
) -> News:
    """
    Creates a news object \n
    Authentication required \n
    Authenticated user must be superuser \n
    """
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
    user:           User = Depends(admin_user),
) -> News:
    """
    Updates a news object by id \n
    Authentication required \n
    Authenticated user must be superuser \n
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
    user:           User = Depends(admin_user),
) -> News:
    """
    Partially updates a news object by id \n
    Authentication required \n
    Authenticated user must be superuser \n
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
async def delete_news_object(
    news_id:    int, 
    db:         AsyncSession = Depends(get_db),
    user:       User = Depends(admin_user),
    ) -> None:
    """
    Deletes a news object by id \n
    Authentication required \n
    Authenticated user must be superuser \n
    """
    return await NewsService.delete_news(db=db, news_id=news_id)
