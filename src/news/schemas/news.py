"""
Pydantic schemas for News
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from .categories import CategoryReadSchema
from .comments import CommentReadSchema


class NewsReadSchema(BaseModel):
    """
    News read schema
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str | None = None
    images: list[str | None]
    created: datetime
    updated: datetime
    category_id: int | None = None


class NewsReadDetailsSchema(NewsReadSchema):
    """
    News read schema with detailed category data
    """

    model_config = ConfigDict(from_attributes=True)

    category: CategoryReadSchema | None = None
    comments: list[CommentReadSchema] = []
