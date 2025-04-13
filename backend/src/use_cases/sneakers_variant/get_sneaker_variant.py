from typing import Callable

from schemas.sneaker_variant.sneaker_variant import SneakerVariantOut
from schemas.sneaker_variant.use_cases import GetSneakerVariantInput
from services.sneaker_variant import SneakerVariantService
from use_cases.base import BaseUseCase


class GetSneakerVariantUseCase(BaseUseCase[GetSneakerVariantInput, SneakerVariantOut]):
    def __init__(
            self, sneaker_variant_service_factory: Callable[[], SneakerVariantService]
    ):
        self.sneaker_variant_service = sneaker_variant_service_factory()

    async def execute(
            self, input_data: GetSneakerVariantInput
    ) -> SneakerVariantOut:
        sneaker_variant = await self.sneaker_variant_service.get_sneaker_variant_by_id(input_data.sneaker_variant_id)
        return sneaker_variant.to_read_model()
