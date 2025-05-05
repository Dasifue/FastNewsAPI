"""
Users router
"""

import uuid

from fastapi import APIRouter, HTTPException, Depends
from fastapi_users import FastAPIUsers
from sqlalchemy import select


from src.redis import redis_client, generate_verification_code
from src.celery import send_verification_code as send_code
from src.database import async_session

from .models import User
from .manager import get_user_manager, UserManager
from .auth import auth_backend
from .schemas import UserRead, UserCreate, UserUpdate, VerificationRequestSchema, VerificationSchema

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

@users_router.post("/send-verification-code/", status_code=200)
async def send_verification_code(data: VerificationRequestSchema) -> dict:
    code = generate_verification_code()
    await redis_client.setex(
        name=data.email,
        time=600,
        value=code
    )
    send_code.run_async(args=[data.email, code])
    return {"message": f"Verification code was send to {data.email}"}


@users_router.post("/verify-code/", status_code=200)
async def verify_code(data: VerificationSchema) -> dict:
    stored_code = await redis_client.get(data.email)
    if stored_code is None:
        raise HTTPException(
            status_code=400, detail="Verification code is expired or does not exist"
        )

    if stored_code.decode("utf-8") != data.code:
        raise HTTPException(
            status_code=400, detail="Invalid verification code"
        )

    async with async_session() as session:
        query = select(User).filter(User.email==data.email)
        result = await session.execute(query)
        user = result.scalar_one_or_none()

        if user is None:
            raise HTTPException(
                status_code=404, detail="User not found"
            )
        user.is_verified = True
        await session.commit()
    return {"message": "Account verified"}


@users_router.delete("/users-delete/", status_code=204)
async def delete_user(
    user:           User = Depends(fastapi_users.current_user()),
    user_manager:   UserManager = Depends(get_user_manager)
):  
    await user_manager.delete(user)
    