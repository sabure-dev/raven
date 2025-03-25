from typing import Callable

from fastapi import Depends

from core.dependencies.sneaker_variant.services import get_sneaker_variant_service_factory
from services.sneaker_variant import SneakerVariantService
from use_cases.sneakers_variant.create_sneaker_variant import CreateSneakerVariantUseCase


def get_create_sneaker_variant_use_case(
        sneaker_variant_service_factory: Callable[[], SneakerVariantService] = Depends(
            get_sneaker_variant_service_factory
        ),
) -> CreateSneakerVariantUseCase:
    return CreateSneakerVariantUseCase(sneaker_variant_service_factory)
