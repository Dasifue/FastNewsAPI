"""
Main frogramm module
"""

from fastapi import FastAPI

from src.news import category_router

app = FastAPI()

app.include_router(router=category_router)
