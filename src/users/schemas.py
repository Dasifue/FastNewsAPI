"""
User schemas
"""

import uuid

from fastapi_users import schemas
from pydantic import EmailStr, field_validator
from pydantic import BaseModel


class UserRead(schemas.BaseUser[uuid.UUID]):
    """
    UserRead schema
    """
    full_name: str


class UserCreate(schemas.BaseUserCreate):
    """
    UserCreate schema
    """
    full_name: str
    email: EmailStr
    password: str

    @field_validator("full_name", mode="after")
    @classmethod
    def validate_full_name(cls, value: str) -> str:
        """
        Method validates full_name length
        """
        if len(value) > 100:
            raise ValueError("Full name must be less than 100 chars")
        return value


class UserUpdate(schemas.BaseUserUpdate):
    """
    UserUpdate schema
    """
    full_name: str


class VerificationRequestSchema(BaseModel):

    email: EmailStr

class VerificationSchema(BaseModel):

    email: EmailStr
    code: str