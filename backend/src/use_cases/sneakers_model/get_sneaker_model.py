from typing import List, Callable

from schemas.sneaker_model.sneaker_model import SneakerModelOut
from schemas.sneaker_model.use_cases import GetSneakersModelsInput, GetSneakerModelInput
from services.sneaker_model import SneakerModelService
from use_cases.base import BaseUseCase


class GetSneakersModelsUseCase(BaseUseCase[None, List[SneakerModelOut]]):
    def __init__(self, sneaker_model_service_factory: Callable[[], SneakerModelService]):
        self.sneaker_model_service = sneaker_model_service_factory()

    async def execute(self, input_data: GetSneakersModelsInput) -> List[SneakerModelOut]:
        include_variants = input_data.params.include_variants or False
        sneakers_models = await self.sneaker_model_service.get_sneakers_models_with_filters(
            name=input_data.params.name,
            brand=input_data.params.brand,
            sneaker_model_type=input_data.params.sneaker_model_type,
            min_price=input_data.params.min_price,
            max_price=input_data.params.max_price,
            sizes=input_data.params.sizes,
            search_query=input_data.params.search_query,
            include_variants=include_variants,
            in_stock=input_data.params.in_stock,
            offset=input_data.params.offset,
            limit=input_data.params.limit,
        )
        return [
            sneaker_model.to_read_model(
                include_variants=include_variants,
            )
            for sneaker_model in sneakers_models
        ]


class GetSneakerModelUseCase(BaseUseCase[None, SneakerModelOut]):
    def __init__(self, sneaker_model_service_factory: Callable[[], SneakerModelService]):
        self.sneaker_model_service = sneaker_model_service_factory()

    async def execute(self, input_data: GetSneakerModelInput) -> SneakerModelOut:
        sneaker_model = await self.sneaker_model_service.get_sneaker_model_by_id(input_data.sneaker_model_id)
        return sneaker_model.to_read_model()
