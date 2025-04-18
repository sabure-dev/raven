from typing import Callable, Any

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from core.exceptions import ItemAlreadyExistsException, ItemNotFoundException, InvalidFieldValueException
from core.utils.repository import AbstractRepository
from db.models.sneakers import SneakerVariant
from schemas.sneaker_variant.sneaker_variant import SneakerVariantCreate


class SneakerVariantService:
    def __init__(self, sneaker_variant_factory: Callable[[], AbstractRepository]):
        self._sneaker_variant_repo = sneaker_variant_factory()

    async def _handle_unique_violation(
            self, fields: dict[str, Any],
    ):
        raise ItemAlreadyExistsException("SneakerVariant", fields)

    async def _handle_foreign_key_not_found_violation(
            self, field: str, value: str,
    ):
        raise ItemNotFoundException("SneakerModel", field, value)

    async def _handle_foreign_key_still_referenced(
            self, field: str, constraint: str
    ):
        raise InvalidFieldValueException(field, constraint)

    # ?
    async def get_sneaker_variant_by_id(self, sneaker_variant_id: int) -> SneakerVariant:
        sneaker_variant = await self._sneaker_variant_repo.find_one_by_field(id=sneaker_variant_id)
        if not sneaker_variant:
            raise ItemNotFoundException("SneakerVariant", "id", str(sneaker_variant_id))
        return sneaker_variant

    async def get_all_by_ids(self, ids: list) -> dict[int, SneakerVariant]:
        return await self._sneaker_variant_repo.find_all_by_field("id", ids,
                                                                  options=[selectinload(SneakerVariant.model)])

    async def create_sneaker_variant(self, sneaker_variant: SneakerVariantCreate) -> int:
        sneaker_variant_dict = sneaker_variant.model_dump()
        try:
            sneaker_variant_id = await self._sneaker_variant_repo.create_one(sneaker_variant_dict)
        except IntegrityError as e:
            if "foreign key" in str(e).lower():
                await self._handle_foreign_key_not_found_violation("id", str(sneaker_variant.model_id))

            elif "unique constraint" in str(e).lower():
                await self._handle_unique_violation({
                    "model_id": sneaker_variant.model_id,
                    "size": sneaker_variant.size
                })
            raise
        return sneaker_variant_id

    async def update_quantity_by_delta(self, sneaker_variant_id: int, delta: int) -> SneakerVariant:
        sneaker_variant = await self.get_sneaker_variant_by_id(sneaker_variant_id)
        if sneaker_variant.quantity + delta < 0:
            raise InvalidFieldValueException("SneakerVariant.quantity", "non-negative number")

        updated_sneaker_variant = await self._sneaker_variant_repo.increment_field(
            sneaker_variant_id,
            "quantity",
            delta)
        if updated_sneaker_variant is None:
            raise ItemNotFoundException("SneakerVariant", "id", str(sneaker_variant_id))

        return updated_sneaker_variant

    async def delete_sneaker_variant(self, sneaker_variant_id: int) -> None:
        try:
            success = await self._sneaker_variant_repo.delete_one(sneaker_variant_id)
            if not success:
                raise ItemNotFoundException("SneakerVariant", "id", str(sneaker_variant_id))
        except ItemNotFoundException:
            raise
        except IntegrityError as e:
            if "foreign key" in str(e).lower():
                await self._handle_foreign_key_still_referenced("Order.sneaker_variant_id", "not null")
