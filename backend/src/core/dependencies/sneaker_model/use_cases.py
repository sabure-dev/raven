from typing import Callable

from fastapi import Depends

from core.dependencies.sneaker_model.services import get_sneaker_model_service_factory
from services.sneaker_model import SneakerModelService
from use_cases.sneakers_model.create_sneaker_model import CreateSneakerModelUseCase
from use_cases.sneakers_model.delete_sneaker_model import DeleteSneakerModelUseCase
from use_cases.sneakers_model.get_sneaker_model import (
    GetSneakerModelUseCase,
    GetSneakersModelsUseCase,
)
from use_cases.sneakers_model.update_sneaker_model import UpdateSneakerModelUseCase


def get_create_sneaker_model_use_case(
        sneaker_model_service_factory: Callable[[], SneakerModelService] = Depends(
            get_sneaker_model_service_factory
        ),
) -> CreateSneakerModelUseCase:
    return CreateSneakerModelUseCase(sneaker_model_service_factory)


def get_get_sneaker_model_use_case(
        sneaker_model_service_factory: Callable[[], SneakerModelService] = Depends(
            get_sneaker_model_service_factory
        ),
) -> GetSneakerModelUseCase:
    return GetSneakerModelUseCase(sneaker_model_service_factory)


def get_get_sneakers_models_use_case(
        sneaker_model_service_factory: Callable[[], SneakerModelService] = Depends(
            get_sneaker_model_service_factory
        ),
) -> GetSneakersModelsUseCase:
    return GetSneakersModelsUseCase(sneaker_model_service_factory)


def get_update_sneaker_model_use_case(
        sneaker_model_service_factory: Callable[[], SneakerModelService] = Depends(
            get_sneaker_model_service_factory
        ),
) -> UpdateSneakerModelUseCase:
    return UpdateSneakerModelUseCase(sneaker_model_service_factory)


def get_delete_sneaker_model_use_case(
        sneaker_model_service_factory: Callable[[], SneakerModelService] = Depends(
            get_sneaker_model_service_factory
        ),
) -> DeleteSneakerModelUseCase:
    return DeleteSneakerModelUseCase(sneaker_model_service_factory)
