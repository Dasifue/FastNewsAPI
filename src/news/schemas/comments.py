"""
Pydantic schemas for Comments
"""

from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CommentReadSchema(BaseModel):
    """
    Comment read schema
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    content: str
    user_id: UUID
    news_id: int
    created: datetime
    updated: datetime


class CommentCreateSchema(BaseModel):
    """
    Comment create schema
    """

    model_config = ConfigDict(from_attributes=True)

    content: str
    news_id: int


class CommentUpdateSchema(BaseModel):
    """
    Comment update schema
    """

    model_config = ConfigDict(from_attributes=True)

    content: str
