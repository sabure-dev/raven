from typing import Callable

from schemas.sneaker_model.use_cases import CreateSneakerModelInput
from services.sneaker_model import SneakerModelService
from use_cases.base import BaseUseCase


class CreateSneakerModelUseCase(BaseUseCase[CreateSneakerModelInput, int]):
    def __init__(
            self,
            sneaker_model_service_factory: Callable[[], SneakerModelService],
    ):
        self.sneaker_model_service = sneaker_model_service_factory()

    async def execute(self, input_data: CreateSneakerModelInput) -> int:
        sneaker_model_id = await self.sneaker_model_service.create_sneaker_model(input_data.sneaker_model)
        return sneaker_model_id
