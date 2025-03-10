"""
User manager
"""

import uuid
from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, UUIDIDMixin

from src.environs import USER_MANAGER_SECRET
from src.celery import send_verification_code
from src.redis import generate_verification_code, redis_client
from .models import User, get_user_db


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = USER_MANAGER_SECRET
    verification_token_secret = USER_MANAGER_SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        code = generate_verification_code()
        await redis_client.setex(
            name=user.email,
            time=600,
            value=code
        )
        send_verification_code.apply_async(args=[user.email, code])

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
