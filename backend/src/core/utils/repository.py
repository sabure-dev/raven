from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Type, Optional

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from db.session.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class AbstractRepository(ABC):
    @abstractmethod
    async def create_one(self, data: dict) -> int:
        raise NotImplementedError

    @abstractmethod
    async def find_one_by_id(self, item_id: int) -> Optional[ModelType]:
        raise NotImplementedError

    @abstractmethod
    async def find_all(self) -> list[ModelType]:
        raise NotImplementedError

    @abstractmethod
    async def find_all_with_filters(
            self,
            filters: list | None = None,
            joins: dict | None = None,
            options: list | None = None,
            having: list | None = None,
            offset: int | None = None,
            limit: int | None = None,
    ) -> list[ModelType]:
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, item: ModelType) -> None:
        raise NotImplementedError

    @abstractmethod
    async def find_one_by_field(self, field: str, value: any) -> Optional[ModelType]:
        raise NotImplementedError

    @abstractmethod
    async def update_one(self, item: ModelType, data: dict) -> ModelType:
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository, Generic[ModelType]):
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self._model = model
        self._session = session

    async def create_one(self, data: dict) -> int:
        instance = self._model(**data)
        self._session.add(instance)
        await self._session.commit()
        await self._session.refresh(instance)
        return instance.id

    async def find_one_by_id(self, item_id: int) -> Optional[ModelType]:
        return await self.find_one_by_field('id', item_id)

    async def find_all(self) -> list[ModelType]:
        query = select(self._model)
        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def find_all_with_filters(
            self,
            filters: list | None = None,
            joins: dict | None = None,
            options: list | None = None,
            having: list | None = None,
            offset: int | None = None,
            limit: int | None = None,
    ) -> list[ModelType]:
        query = select(self._model)
        if joins:
            for relation, condition in joins.items():
                if condition is True:
                    query = query.join(getattr(self._model, relation))
                else:
                    query = query.join(getattr(self._model, relation)).where(condition)

        if filters:
            query = query.where(and_(*filters))

        if having:
            query = query.group_by(self._model.id)
            query = query.having(and_(*having))

        if options:
            for option in options:
                query = query.options(option)

        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)

        query = query.distinct()

        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def delete_one(self, item: ModelType) -> None:
        await self._session.delete(item)
        await self._session.commit()

    async def find_one_by_field(self, field: str, value: any) -> Optional[ModelType]:
        query = select(self._model).where(getattr(self._model, field) == value)
        result = await self._session.execute(query)
        return result.scalar_one_or_none()

    async def update_one(self, item: ModelType, data: dict) -> ModelType:
        for key, value in data.items():
            setattr(item, key, value)
        await self._session.commit()
        await self._session.refresh(item)
        return item
