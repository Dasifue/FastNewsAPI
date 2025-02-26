"""
Services module contains business logic
"""

from typing import Sequence
from datetime import datetime

from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from src.manager import DBManager
from src.users import User

from ..models import Comment
from .news import NewsService



class CommentService():

    @classmethod
    async def get_comments(
        cls,
        db: AsyncSession,
        offset: int = 0,
        limit: int = 10,
    ) -> Sequence[Comment]:
        """
        Service
        """
        return await DBManager.get_objects(db, model=Comment, offset=offset, limit=limit)


    @classmethod
    async def get_comment(
        cls,
        db: AsyncSession,
        comment_id: int,

    ) -> Comment:
        """
        Service
        """
        comment = await DBManager.get_object(db=db, model=Comment, field="id", value=comment_id)
        if comment is None:
            raise HTTPException(status_code=404, detail="Comment not found")
        return comment


    @classmethod
    async def create_comment(
        cls,
        db: AsyncSession,
        comment: dict,
        user: User,
    ) -> Comment:
        """
        Service
        """
        await NewsService.get_news_object(db, comment["news_id"])

        comment["user_id"] = user.id
        return await DBManager.create_object(**comment, db=db, model=Comment, commit=True)


    @classmethod
    async def delete_comment(
        cls,
        db: AsyncSession,
        comment_id: int,
        user: User,
    ) -> None:
        """
        Service
        """

        comment = await DBManager.get_objects(db, model=Comment, field="id", value=comment_id)
        if comment.user_id != user.id:
            raise HTTPException(status_code=403, detail="You are not allowed to delete this comment")

        await DBManager.delete_object(db=db, model=Comment, field="id", value=comment_id, commit=False)


    @classmethod
    async def update_comment(
        cls,
        db: AsyncSession,
        comment_id: int,
        comment: dict,
        user: User,
    ) -> Comment:
        """
        Service
        """

        comment['updated_at'] = datetime.utcnow()
        comment: Comment = await DBManager.update_object(**comment, db=db, model=Comment, field="id", value=comment_id, commit=False)

        if comment is None:
            raise HTTPException(status_code=404, detail="Comment not found")

        if comment.user_id != user.id:
            raise HTTPException(status_code=403, detail="You are not allowed to update this comment")

        await db.commit()
        await db.refresh(comment)
        return comment


    @classmethod
    async def partial_update_comment(
        cls,
        db: AsyncSession,
        comment_id: int,
        comment: dict,
        user: User,
    ) -> Comment:
        """
        Service
        """

        if comment["category_id"]:
            await NewsService.get_news_object(db, comment["news_id"])

        comment['updated_at'] = datetime.utcnow()
        comment: Comment = await DBManager.partial_update_object(**comment, db=db, model=Comment, field="id", value=comment_id, commit=True)

        if comment is None:
            raise HTTPException(status_code=404, detail="Comment not found")

        if comment.user_id != user.id:
            raise HTTPException(status_code=403, detail="You are not allowed to update this comment")

        await db.commit()
        await db.refresh(comment)
        return comment
