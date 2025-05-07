"""
Pydantic schemas for Categories
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CategoryReadSchema(BaseModel):
    """
    Category read schema
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    created: datetime


class CategoryCreateSchema(BaseModel):
    """
    Category create schema
    """

    model_config = ConfigDict(from_attributes=True)

    name: str
