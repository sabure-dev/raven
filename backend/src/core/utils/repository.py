from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Type, Optional, Any

from sqlalchemy import select, and_, update, delete, insert
from sqlalchemy.ext.asyncio import AsyncSession

from db.session.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class AbstractRepository(ABC):
    @abstractmethod
    async def create_one(self, data: dict) -> ModelType:
        raise NotImplementedError

    @abstractmethod
    async def find_all_with_filters(
            self,
            filters: list | None = None,
            joins: dict | None = None,
            options: list | None = None,
            offset: int | None = None,
            limit: int | None = None,
    ) -> list[ModelType]:
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, item_id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def find_one_by_field(self, **filters: Any) -> Optional[ModelType]:
        raise NotImplementedError

    @abstractmethod
    async def update_one(self, item_id: int, data: dict) -> ModelType:
        raise NotImplementedError

    @abstractmethod
    async def increment_field(
            self,
            item_id: int,
            field: str,
            delta: int) -> ModelType | None:
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository, Generic[ModelType]):
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self._model = model
        self._session = session

    # Транзакции можно будет расписать на уровне сервисов, а тут юзать flush вместо commit! (но нужно будет прокинуть сессию)
    async def create_one(self, data: dict) -> ModelType:
        stmt = insert(self._model).values(**data).returning(self._model)
        result = await self._session.execute(stmt)
        await self._session.commit()
        return result.scalar_one()

    async def find_all_with_filters(
            self,
            filters: list | None = None,
            joins: dict | None = None,
            options: list | None = None,
            offset: int | None = None,
            limit: int | None = None,
    ) -> list[ModelType]:
        query = select(self._model).distinct()
        if joins:
            for relation, condition in joins.items():
                if condition is True:
                    query = query.join(getattr(self._model, relation))
                else:
                    query = query.join(getattr(self._model, relation)).where(condition)

        if filters:
            query = query.where(and_(*filters))

        if options:
            for option in options:
                query = query.options(option)

        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)

        result = await self._session.execute(query)
        return list(result.unique().scalars().all())

    async def delete_one(self, item_id: int) -> bool:
        stmt = delete(self._model).where(self._model.id == item_id)
        result = await self._session.execute(stmt)
        await self._session.commit()
        return result.rowcount > 0

    async def find_one_by_field(self, **filters: Any) -> Optional[ModelType]:
        query = select(self._model).filter_by(**filters)
        result = await self._session.execute(query)
        return result.scalar_one_or_none()

    async def update_one(self, item_id: int, data: dict) -> ModelType:
        stmt = (
            update(self._model)
            .where(self._model.id == item_id)
            .values(**data)
            .returning(self._model)
        )
        result = await self._session.execute(stmt)
        updated_item = result.scalar_one()
        await self._session.commit()
        return updated_item

    async def increment_field(
            self,
            item_id: int,
            field: str,
            delta: int
    ) -> ModelType | None:
        model_field = getattr(self._model, field)
        new_value = model_field + delta
        where_condition = and_(self._model.id == item_id, new_value >= 0)

        stmt = (
            update(self._model)
            .where(where_condition)
            .values({field: new_value})
            .returning(self._model)
        )

        result = await self._session.execute(stmt)
        updated_item = result.scalar_one_or_none()
        await self._session.commit()
        return updated_item
