from typing import Callable, Any, Literal

from sqlalchemy import or_, and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from core.exceptions import (
    ItemAlreadyExistsException,
    ItemNotFoundException,
    NoDataProvidedException,
)
from core.utils.repository import AbstractRepository
from db.models.sneakers import SneakerModel, SneakerVariant
from schemas.sneaker_model.sneaker_model import SneakerModelCreate, SneakerModelUpdate


class SneakerModelService:
    def __init__(self, sneaker_model_factory: Callable[[], AbstractRepository]):
        self._sneaker_model_repo = sneaker_model_factory()

    async def _handle_unique_violation(
            self, fields: dict[str, Any],
    ):
        raise ItemAlreadyExistsException("SneakerModel", fields)

    async def create_sneaker_model(self, sneaker_model: SneakerModelCreate) -> SneakerModel:
        sneaker_model_dict = sneaker_model.model_dump()
        try:
            sneaker = await self._sneaker_model_repo.create_one(sneaker_model_dict)
        except IntegrityError as e:
            if "unique constraint" in str(e).lower():
                await self._handle_unique_violation({"name": sneaker_model.name})
            raise

        return sneaker

    async def get_sneakers_models_with_filters(
            self,
            sneaker_model_id: int | None = None,
            name: str | None = None,
            brand: str | None = None,
            sneaker_model_type: str | None = None,
            min_price: float | None = None,
            max_price: float | None = None,
            sizes: list[float] | None = None,
            search_query: str | None = None,
            include_variants: bool = False,
            in_stock: bool | None = None,
            offset: int | None = None,
            limit: int | None = None,
            sort_by_price: Literal["asc", "desc"] | None = None,
    ) -> list[SneakerModel]:
        filters = []
        variant_filters = []
        options = []
        joins = {}

        if sneaker_model_id:
            filters.append(SneakerModel.id == sneaker_model_id)
        if name:
            filters.append(SneakerModel.name == name)
        if brand:
            filters.append(SneakerModel.brand == brand)
        if sneaker_model_type:
            filters.append(SneakerModel.type == sneaker_model_type)
        if min_price is not None:
            filters.append(SneakerModel.price >= min_price)
        if max_price is not None:
            filters.append(SneakerModel.price <= max_price)

        if sizes:
            variant_filters.append(SneakerVariant.size.in_(sizes))

        if in_stock is not None:
            variant_condition = (
                SneakerVariant.quantity > 0
                if in_stock
                else SneakerVariant.quantity == 0
            )
            variant_filters.append(variant_condition)

        if variant_filters:
            joins["variants"] = and_(*variant_filters)

        if search_query:
            search_pattern = f"%{search_query}%"
            filters.append(
                or_(
                    SneakerModel.name.ilike(search_pattern),
                    SneakerModel.description.ilike(search_pattern),
                )
            )

        if include_variants:
            options.append(joinedload(SneakerModel.variants))

        return await self._sneaker_model_repo.find_all_with_filters(
            filters=filters,
            joins=joins,
            options=options,
            offset=offset,
            limit=limit,
            order_by=("price", sort_by_price) if sort_by_price else None,
        )

    async def update_sneaker_model(
            self, sneaker_model_id: int, update_sneaker_model: SneakerModelUpdate
    ) -> SneakerModel:
        update_values = update_sneaker_model.model_dump(exclude_unset=True)

        if not update_values:
            raise NoDataProvidedException()

        try:
            updated_sneaker_model = await self._sneaker_model_repo.update_one(
                sneaker_model_id, update_values
            )
        except IntegrityError as e:
            if "unique constraint" in str(e).lower():
                await self._handle_unique_violation({"name": update_sneaker_model.name})
            raise

        return updated_sneaker_model

    async def delete_sneaker_model(self, sneaker_model_id: int) -> None:
        success = await self._sneaker_model_repo.delete_one(sneaker_model_id)
        if not success:
            raise ItemNotFoundException("SneakerModel", "id", str(sneaker_model_id))
