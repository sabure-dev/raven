from typing import Callable

from fastapi import Depends

from core.dependencies.sneaker_model.database import get_sneaker_model_repository_factory
from repositories.sneakers import SneakerModelRepository
from services.sneaker_model import SneakerModelService


def get_sneaker_model_service_factory(
        sneaker_model_repository_factory: Callable[[], SneakerModelRepository] = Depends(
            get_sneaker_model_repository_factory)
) -> Callable[[], SneakerModelService]:
    return lambda: SneakerModelService(sneaker_model_repository_factory)
