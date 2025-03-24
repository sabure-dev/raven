from typing import Callable, Any

from sqlalchemy.exc import IntegrityError

from core.exceptions import ItemAlreadyExistsException
from core.utils.repository import AbstractRepository
from schemas.sneaker_variant.sneaker_variant import SneakerVariantCreate


class SneakerVariantService:
    def __init__(self, sneaker_variant_factory: Callable[[], AbstractRepository]):
        self.sneaker_variant_repo = sneaker_variant_factory()

    async def _handle_unique_violation(
            self, error: IntegrityError, fields: dict[str, Any],
    ):
        if "unique constraint" in str(error).lower():
            raise ItemAlreadyExistsException("SneakerVariant", fields)
        raise

    async def create_sneaker_variant(self, sneaker_variant: SneakerVariantCreate) -> int:
        sneaker_variant_dict = sneaker_variant.model_dump()
        try:
            sneaker_variant_id = await self.sneaker_variant_repo.create_one(sneaker_variant_dict)
        except IntegrityError as e:
            if "model_id" in str(e).lower() and "size" in str(e).lower():
                await self._handle_unique_violation(e, {
                    "model_id": sneaker_variant.model_id,
                    "size": sneaker_variant.size
                })
            raise
        return sneaker_variant_id
