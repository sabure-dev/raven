from typing import Callable

from sqlalchemy import or_, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from core.utils.repository import AbstractRepository
from db.models.sneakers import SneakerModel, SneakerVariant
from schemas.sneaker_model import SneakerModelCreate
from core.exceptions import ItemAlreadyExistsException, ItemNotFoundException


class SneakerModelService:
    def __init__(self, sneaker_model_factory: Callable[[], AbstractRepository]):
        self.sneaker_model_repo = sneaker_model_factory()

    async def _handle_unique_violation(self, error: IntegrityError, field: str, value: str):
        if "unique constraint" in str(error).lower():
            raise ItemAlreadyExistsException('SneakerModel', field, value)
        raise

    async def create_sneakers_model(self, sneaker_model: SneakerModelCreate) -> (int, SneakerModel):
        sneaker_model_dict = sneaker_model.model_dump()
        try:
            sneaker_id = await self.sneaker_model_repo.create_one(sneaker_model_dict)
        except IntegrityError as e:
            if 'name' in str(e).lower():
                await self._handle_unique_violation(e, 'name', sneaker_model.name)
            raise

        created_sneaker_model = SneakerModel(**sneaker_model_dict)
        created_sneaker_model.id = sneaker_id

        return sneaker_id, created_sneaker_model

    async def get_sneakers_models_with_filters(
            self,
            name: str | None = None,
            brand: str | None = None,
            sneaker_type: str | None = None,
            min_price: float | None = None,
            max_price: float | None = None,
            sizes: list[float] | None = None,
            search_query: str | None = None,
            include_variants: bool = False,
            in_stock: bool | None = None,
            offset: int | None = None,
            limit: int | None = None
    ) -> list[SneakerModel]:
        filters = []
        joins = {}
        having = []
        options = []

        if name:
            filters.append(SneakerModel.name == name)
        if brand:
            filters.append(SneakerModel.brand == brand)
        if sneaker_type:
            filters.append(SneakerModel.type == sneaker_type)

        if min_price is not None:
            filters.append(SneakerModel.price >= min_price)
        if max_price is not None:
            filters.append(SneakerModel.price <= max_price)

        if search_query:
            search_filter = or_(
                SneakerModel.name.ilike(f"%{search_query}%"),
                SneakerModel.description.ilike(f"%{search_query}%")
            )
            filters.append(search_filter)

        if sizes:
            joins[SneakerModel.variants] = SneakerVariant.size.in_(sizes)

        if include_variants:
            options.append(joinedload(SneakerModel.variants))

        if in_stock is not None:
            joins[SneakerModel.variants] = True
            if in_stock:
                having.append(func.sum(SneakerVariant.quantity) > 0)
            else:
                having.append(func.sum(SneakerVariant.quantity) == 0)

        return await self.sneaker_model_repo.find_all_with_filters(
            filters=filters,
            joins=joins if joins else None,
            options=options,
            having=having if having else None,
            offset=offset,
            limit=limit
        )

    async def get_sneaker_model_by_id(self, sneaker_model_id: int) -> SneakerModel:
        sneaker_model = await self.sneaker_model_repo.find_one_by_id(sneaker_model_id)
        if not sneaker_model:
            raise ItemNotFoundException('SneakerModel', 'id', str(sneaker_model_id))
        return sneaker_model

    async def update_sneaker_model(self, sneaker_model_id: int,
                                   new_sneaker_model: SneakerModelCreate) -> SneakerModel:
        sneaker_model = await self.get_sneaker_model_by_id(sneaker_model_id)
        try:
            updated_sneaker_model = await self.sneaker_model_repo.update_one(
                sneaker_model,
                new_sneaker_model.model_dump()
            )
        except IntegrityError as e:
            await self._handle_unique_violation(e, 'name', new_sneaker_model.name)
            raise

        return updated_sneaker_model

    async def delete_sneaker_model(self, sneaker_model_id: int) -> None:
        user = await self.get_sneaker_model_by_id(sneaker_model_id)
        await self.sneaker_model_repo.delete_one(user)
