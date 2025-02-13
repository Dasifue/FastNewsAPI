"""
__init__.py
"""

from .categories import router as categories_router
from .news import router as news_router

__all__ = [
    "categories_router",
    "news_router",
]
