from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Type, Optional, List, Sequence

from sqlalchemy import select
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
    async def find_all(self) -> Sequence[ModelType]:
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, item_id: int) -> None:
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
        query = select(self._model).where(self._model.id == item_id)
        result = await self._session.execute(query)
        result = result.scalar_one_or_none()
        if result:
            return result
        return None

    async def find_all(self) -> Sequence[ModelType]:
        query = select(self._model)
        result = await self._session.execute(query)
        return result.scalars().all()

    async def delete_one(self, item_id: int) -> None:
        instance = await self.find_one_by_id(item_id)
        if instance:
            await self._session.delete(instance)
            await self._session.commit()
