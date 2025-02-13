"""
__init__.py
"""

from .categories import CategoryCreateSchema, CategoryReadSchema
from .news import NewsReadSchema

__all__ = [
    "CategoryCreateSchema",
    "CategoryReadSchema",
    "NewsReadSchema",
]
