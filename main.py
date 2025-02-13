"""
Main program module
"""

from fastapi import FastAPI

from src.news import routers
from src.users import users_router

app = FastAPI()

app.include_router(router=routers.categories_router)
app.include_router(router=routers.news_router)
app.include_router(router=users_router)
