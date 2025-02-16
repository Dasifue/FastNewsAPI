"""
Main program module
"""

from fastapi import FastAPI

from src.news import routers
from src.users import users_router
from src.media import media_router

app = FastAPI()

app.include_router(router=routers.categories_router)
app.include_router(router=routers.news_router)
app.include_router(router=users_router)
app.include_router(router=media_router)
