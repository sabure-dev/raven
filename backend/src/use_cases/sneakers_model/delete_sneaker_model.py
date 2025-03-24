from typing import Callable

from schemas.sneaker_model.use_cases import DeleteSneakerModelInput
from services.sneaker_model import SneakerModelService
from use_cases.base import BaseUseCase


class DeleteSneakerModelUseCase(BaseUseCase[DeleteSneakerModelInput, None]):
    def __init__(
            self, sneaker_model_service_factory: Callable[[], SneakerModelService]
    ):
        self.sneaker_model_service = sneaker_model_service_factory()

    async def execute(self, input_data: DeleteSneakerModelInput) -> None:
        await self.sneaker_model_service.delete_sneaker_model(
            input_data.sneaker_model_id
        )
