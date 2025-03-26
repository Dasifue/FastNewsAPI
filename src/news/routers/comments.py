"""
Comments Router
"""

from typing import Sequence

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Comment
from ..schemas import CommentReadSchema, CommentCreateSchema, CommentUpdateSchema
from ..services import CommentService

from src.database import get_db
from src.redis import cache
from src.users import fastapi_users, User

router = APIRouter(
    prefix="/comments",
    tags=["Comments"]
)

authenticated_user = fastapi_users.current_user(active=True)


@router.get("", response_model=Sequence[CommentReadSchema])
@cache(60 * 5)
async def get_comments(offset: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)) -> Sequence[Comment]:
    """
    Get all comments \n
    No authentication required \n
    """
    return await CommentService.get_comments(db, offset, limit)


@router.get("/{comment_id}", response_model=CommentReadSchema)
@cache(60 * 5)
async def get_comment(comment_id: int, db: AsyncSession = Depends(get_db)) -> Comment:
    """
    Get comment by id \n
    No authentication required \n
    """
    return await CommentService.get_comment(db, comment_id)


@router.post("", response_model=CommentReadSchema)
async def create_comment(
    comment:    CommentCreateSchema,
    db:         AsyncSession = Depends(get_db),
    user:       User = Depends(authenticated_user),
) -> Comment:
    """
    Create comment \n
    Authentication required \n
    """
    return await CommentService.create_comment(db, comment.dict(), user=user)


@router.put("/{comment_id}", response_model=CommentReadSchema)
async def update_comment(
    comment_id: int,
    comment:    CommentUpdateSchema,
    db:         AsyncSession = Depends(get_db),
    user:       User = Depends(authenticated_user),
) -> Comment:
    """
    Update comment \n
    Authentication required \n
    Authenticated user must be the owner of the comment \n
    """
    return await CommentService.update_comment(db, comment_id, comment.dict(), user=user)


@router.patch("/{comment_id}", response_model=CommentReadSchema)
async def update_comment(
    comment_id: int,
    comment:    CommentUpdateSchema,
    db:         AsyncSession = Depends(get_db),
    user:       User = Depends(authenticated_user),
) -> Comment:
    """
    Update comment \n
    Authentication required \n
    Authenticated user must be the owner of the comment \n
    """
    return await CommentService.partial_update_comment(db, comment_id, comment.dict(), user=user)


@router.delete("/{comment_id}", status_code=204)
async def delete_comment(
    comment_id: int, 
    db:         AsyncSession = Depends(get_db),
    user:       User = Depends(authenticated_user),
) -> None:
    """
    Delete comment by id \n
    Authentication required \n
    Authenticated user must be the owner of the comment \n
    """
    return await CommentService.delete_comment(db, comment_id, user=user)
