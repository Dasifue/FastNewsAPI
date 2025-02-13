"""
Users router
"""

import uuid

from fastapi import APIRouter
from fastapi_users import FastAPIUsers

from .models import User
from .manager import get_user_manager
from .auth import auth_backend
from .schemas import UserRead, UserCreate, UserUpdate

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

users_router = APIRouter()

users_router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

users_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

users_router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
