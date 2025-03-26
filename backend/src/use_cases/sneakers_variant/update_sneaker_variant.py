from typing import Callable

from services.sneaker_variant import SneakerVariantService
from schemas.sneaker_variant.sneaker_variant import SneakerVariantOut
from schemas.sneaker_variant.use_cases import UpdateSneakerVariantQuantityInput
from use_cases.base import BaseUseCase


class UpdateSneakerVariantQuantityUseCase(BaseUseCase[UpdateSneakerVariantQuantityInput, SneakerVariantOut]):
    def __init__(
            self,
            sneaker_variant_service_factory: Callable[[], SneakerVariantService],
    ):
        self.sneaker_variant_service = sneaker_variant_service_factory()

    async def execute(self, input_data: UpdateSneakerVariantQuantityInput) -> SneakerVariantOut:
        updated_sneaker_variant = await self.sneaker_variant_service.update_quantity_by_delta(
            input_data.sneaker_variant_id,
            input_data.quantity_delta,
        )
        return updated_sneaker_variant.to_read_model()
