"""
DB models Manager
"""

from typing import Sequence, Type, Any

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from .database import Base

class DBManager():

    @staticmethod
    async def get_objects(
        db: AsyncSession,
        model: Type[Base],
        filters: dict[str, Any] | None = None,
        offset: int = 0,
        limit: int = 10
    ) -> Sequence[Base]:
        """
        Возвращает список объектов с фильтрацией
        """
        query = select(model)

        if filters:
            for field, value in filters.items():
                query = query.where(getattr(model, field) == value)

        query = query.offset(offset).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()


    @staticmethod
    async def get_object(
        db: AsyncSession,
        model: Type[Base],
        field: str,
        value: Any,
        option: Any = None,
    ) -> Base | None:
        """
        Возвращает объект по указанному полю (не обязательно id)
        """
        query = select(model).where(getattr(model, field) == value)
        if option:
            query = query.options(option)
        
        result = await db.execute(query)
        return result.scalar_one_or_none()


    @staticmethod
    async def create_object(
        db: AsyncSession,
        model: Type[Base],
        commit: bool = False,
        **kwargs
    ) -> Base:
        """
        Создаёт объект в БД
        """
        instance = model(**kwargs)
        db.add(instance)

        if commit:
            await db.commit()
            await db.refresh(instance)

        return instance


    @staticmethod
    async def delete_object(
        db: AsyncSession,
        model: type[Base],
        field: str,
        value: Any,
        commit: bool = False,
    ) -> None:
        """
        Method deletes a model instance
        """
        query = delete(model).where(getattr(model, field)==value)
        await db.execute(query)

        if commit:
            await db.commit()


    @staticmethod
    async def update_object(
        db: AsyncSession,
        model: Type[Base],
        field: str,
        value: Any,
        commit: bool = False,
        **kwargs
    ) -> Base | None:
        """
        Method updates a model instance
        """
        query = select(model).where(getattr(model, field) == value)
        result = await db.execute(query)
        instance = result.scalar_one_or_none()

        if instance is None:
            return None

        for field, value in kwargs.items():
            setattr(instance, field, value)

        if commit:
            await db.commit()
            await db.refresh(instance)

        return instance


    @staticmethod
    async def partial_update_object(
        db: AsyncSession,
        model: Type[Base],
        field: str,
        value: Any,
        commit: bool = False,
        **kwargs
    ) -> Base | None:
        """
        Method partially updates a model instance
        """
        query = select(model).where(getattr(model, field) == value)
        result = await db.execute(query)
        instance = result.scalar_one_or_none()

        if instance is None:
            return None

        for field, value in kwargs.items():
            if field in model.__table__.columns and value:
                setattr(instance, field, value)

        if commit:
            await db.commit()
            await db.refresh(instance)

        return instance
