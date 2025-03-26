from typing import Callable

from schemas.sneaker_variant.use_cases import DeleteSneakerVariantInput
from services.sneaker_variant import SneakerVariantService
from use_cases.base import BaseUseCase


class DeleteSneakerVariantUseCase(BaseUseCase[DeleteSneakerVariantInput, None]):
    def __init__(
            self, sneaker_variant_service_factory: Callable[[], SneakerVariantService]
    ):
        self.sneaker_variant_service = sneaker_variant_service_factory()

    async def execute(self, input_data: DeleteSneakerVariantInput) -> None:
        await self.sneaker_variant_service.delete_sneaker_variant(
            input_data.sneaker_variant_id
        )
