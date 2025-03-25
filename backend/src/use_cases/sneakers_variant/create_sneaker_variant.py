from typing import Callable

from schemas.sneaker_variant.use_cases import CreateSneakerVariantInput
from services.sneaker_variant import SneakerVariantService
from use_cases.base import BaseUseCase


class CreateSneakerVariantUseCase(BaseUseCase[CreateSneakerVariantInput, int]):
    def __init__(
            self,
            sneaker_variant_service_factory: Callable[[], SneakerVariantService],
    ):
        self.sneaker_model_service = sneaker_variant_service_factory()

    async def execute(self, input_data: CreateSneakerVariantInput) -> int:
        sneaker_variant_id = await self.sneaker_model_service.create_sneaker_variant(
            input_data.sneaker_variant
        )
        return sneaker_variant_id
