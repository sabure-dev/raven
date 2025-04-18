from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Type, Optional, Any, Literal

from sqlalchemy import select, and_, update, delete, insert
from sqlalchemy.ext.asyncio import AsyncSession

from db.session.base import Base

ModelType = TypeVar("ModelType", bound=Base)
OrderByType = tuple[str, Literal["asc", "desc"]]


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
            order_by: OrderByType | None = None
    ) -> list[ModelType]:
        raise NotImplementedError

    @abstractmethod
    async def find_all_by_field(self, field: str, values: list, options: list | None = None) -> dict[any, ModelType]:
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, item_id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def find_one_by_field(self, options: list | None = None, **filters: Any) -> Optional[ModelType]:
        raise NotImplementedError

    @abstractmethod
    async def update_one(self, item_id: int, data: dict) -> ModelType:
        raise NotImplementedError

    @abstractmethod
    async def increment_field(
            self,
            item_id: int,
            field: str,
            delta: float) -> ModelType | None:
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository, Generic[ModelType]):
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self._model = model
        self._session = session

    async def create_one(self, data: dict) -> ModelType:
        stmt = insert(self._model).values(**data).returning(self._model)
        result = await self._session.execute(stmt)
        return result.scalar_one()

    async def find_all_with_filters(
            self,
            filters: list | None = None,
            joins: dict | None = None,
            options: list | None = None,
            offset: int | None = None,
            limit: int | None = None,
            order_by: OrderByType | None = None,
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

        if order_by:
            field, direction = order_by
            field = getattr(self._model, field)
            if direction == "asc":
                query = query.order_by(field.asc())
            else:
                query = query.order_by(field.desc())
        else:
            query = query.order_by(self._model.id.desc())

        if options:
            for option in options:
                query = query.options(option)

        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)

        result = await self._session.execute(query)
        return list(result.unique().scalars().all())

    async def find_all_by_field(self, field: str, values: list, options: list | None = None) -> dict[any, ModelType]:
        if not values:
            return {}
        model_field = getattr(self._model, field)
        stmt = select(self._model).where(model_field.in_(values))
        if options:
            for option in options:
                stmt = stmt.options(option)

        result = await self._session.execute(stmt)
        return {item.id: item for item in result.scalars()}

    async def delete_one(self, item_id: int) -> bool:
        stmt = delete(self._model).where(self._model.id == item_id)
        result = await self._session.execute(stmt)
        return result.rowcount > 0

    async def find_one_by_field(self, options: list | None = None, **filters: Any) -> Optional[ModelType]:
        query = select(self._model).filter_by(**filters)
        if options:
            for option in options:
                query = query.options(option)
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
        return result.scalar_one()

    async def increment_field(
            self,
            item_id: int,
            field: str,
            delta: float
    ) -> ModelType | None:
        model_field = getattr(self._model, field)
        new_value = model_field + delta
        where_condition = self._model.id == item_id

        stmt = (
            update(self._model)
            .where(where_condition)
            .values({field: new_value})
            .returning(self._model)
        )

        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()
