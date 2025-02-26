"""
Pydantic schemas for Comments
"""

from uuid import UUID
from datetime import datetime

from pydantic import BaseModel


class CommentReadSchema(BaseModel):
    """
    Comment read schema
    """
    id: int
    content: str
    user_id: UUID
    news_id: int
    created: datetime
    updated: datetime

    class Config:
        from_attributes = True


class CommentCreateSchema(BaseModel):
    """
    Comment create schema
    """
    content: str
    news_id: int

    class Config:
        from_attributes = True


class CommentUpdateSchema(BaseModel):
    """
    Comment update schema
    """
    content: str

    class Config:
        from_attributes = True