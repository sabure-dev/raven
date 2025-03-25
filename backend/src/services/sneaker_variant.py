from typing import Callable, Any

from asyncpg import ForeignKeyViolationError
from sqlalchemy.exc import IntegrityError

from core.exceptions import ItemAlreadyExistsException, ItemNotFoundException
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

    async def _handle_foreign_key_violation(
            self, field: str, value: str,
    ):
        raise ItemNotFoundException("SneakerModel", field, value)

    async def create_sneaker_variant(self, sneaker_variant: SneakerVariantCreate) -> int:
        sneaker_variant_dict = sneaker_variant.model_dump()
        try:
            sneaker_variant_id = await self._sneaker_variant_repo.create_one(sneaker_variant_dict)
        except IntegrityError as e:
            if "foreign key" in str(e).lower():
                await self._handle_foreign_key_violation("id", str(sneaker_variant.model_id))

            elif "unique constraint" in str(e).lower():
                await self._handle_unique_violation({
                    "model_id": sneaker_variant.model_id,
                    "size": sneaker_variant.size
                })
            raise
        return sneaker_variant_id

    async def delete_sneaker_variant(self, sneaker_variant_id: int) -> None:
        success = await self._sneaker_variant_repo.delete_one(sneaker_variant_id)
        if not success:
            raise ItemNotFoundException("SneakerVariant", "id", str(sneaker_variant_id))

    async def update_quantity_by_delta_sneaker_variant(self, sneaker_variant_id: int, delta: int) -> SneakerVariant:
        updated_sneaker_variant = await self._sneaker_variant_repo.increment_field(
            sneaker_variant_id,
            "quantity",
            delta)
        if updated_sneaker_variant is None:
            raise ValueError("sneaker_variant quantity can't be negative")
        return updated_sneaker_variant
