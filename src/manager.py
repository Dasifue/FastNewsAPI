"""
DB models Mabager
"""

from typing import Sequence
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select, delete

from pydantic import BaseModel

from .database import session as async_session, Base

class DBManager():

    @classmethod
    async def get_objects(
        cls,
        model: type[Base],
        offset: int = 0,
        limit: int = 10
    ) -> Sequence[Base]:
        """
        Method returns an array of objects
        """
        async with async_session() as session:
            query = select(model).offset(offset).limit(limit)
            result = await session.execute(query)
            objects = result.scalars().all()
            return objects
    
    @classmethod
    async def get_object(
        cls,
        model: type[Base],
        object_id: int | UUID,
    ) -> type[Base] | None:
        """
        Method returns a model instance
        """
        async with async_session() as session:
            query = select(model).where(model.id==object_id)
            result = await session.execute(query)
            _object = result.scalar_one_or_none()
            return _object


    @classmethod
    async def create_object(
        cls,
        instance: type[Base]
    ) -> type[Base]:
        """
        Method for object creation
        """
        async with async_session() as session:
            session.add(instance=instance)
            await session.commit()
            await session.refresh(instance=instance)
            return instance
    

    @classmethod
    async def delete_object(
        cls,
        model: type[Base],
        object_id: int | UUID,
    ) -> None:
        """
        Method deletes a model instance
        """
        async with async_session() as session:
            query = delete(model).where(model.id==object_id)
            await session.execute(query)
            await session.commit()


    @classmethod
    async def update_object(
        cls,
        model: type[Base],
        object_id: int | UUID,
        updated_data: type[BaseModel]
    ) -> type[Base]:
        """
        Method updates a model instance
        """
        async with async_session() as session:
            query = select(model).filter(model.id == object_id)
            result = await session.execute(query)
            old_object = result.scalar_one_or_none()
            if old_object is None:
                raise HTTPException(status_code=404, detail=f"{model.__name__} not found")

            for field, value in updated_data.dict().items():
                setattr(old_object, field, value)

            await session.commit()
            await session.refresh(old_object)
            return old_object


    @classmethod
    async def partial_update_object(
        cls,
        model: type[Base],
        object_id: int | UUID,
        updated_data: type[BaseModel]
    ) -> type[Base]:
        """
        Method partially updates a model instance
        """
        async with async_session() as session:
            query = select(model).filter(model.id == object_id)
            result = await session.execute(query)
            old_object = result.scalar_one_or_none()
            if old_object is None:
                raise HTTPException(status_code=404, detail=f"{model.__name__} not found")

            for field, value in updated_data.dict().items():
                if value:
                    setattr(old_object, field, value)

            await session.commit()
            await session.refresh(old_object)
            return old_object
