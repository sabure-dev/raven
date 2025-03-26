from typing import Callable

from fastapi import Depends

from core.dependencies.sneaker_variant.services import get_sneaker_variant_service_factory
from services.sneaker_variant import SneakerVariantService
from use_cases.sneakers_variant.create_sneaker_variant import CreateSneakerVariantUseCase
from use_cases.sneakers_variant.delete_sneaker_variant import DeleteSneakerVariantUseCase
from use_cases.sneakers_variant.update_sneaker_variant import UpdateSneakerVariantQuantityUseCase


def get_create_sneaker_variant_use_case(
        sneaker_variant_service_factory: Callable[[], SneakerVariantService] = Depends(
            get_sneaker_variant_service_factory
        ),
) -> CreateSneakerVariantUseCase:
    return CreateSneakerVariantUseCase(sneaker_variant_service_factory)


def get_update_sneaker_variant_quantity_use_case(
        sneaker_variant_service_factory: Callable[[], SneakerVariantService] = Depends(
            get_sneaker_variant_service_factory
        ),
) -> UpdateSneakerVariantQuantityUseCase:
    return UpdateSneakerVariantQuantityUseCase(sneaker_variant_service_factory)


def get_delete_sneaker_variant_use_case(
        sneaker_variant_service_factory: Callable[[], SneakerVariantService] = Depends(
            get_sneaker_variant_service_factory
        ),
) -> DeleteSneakerVariantUseCase:
    return DeleteSneakerVariantUseCase(sneaker_variant_service_factory)
