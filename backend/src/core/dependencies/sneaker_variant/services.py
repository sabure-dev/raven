from typing import Callable

from fastapi import Depends

from core.dependencies.sneaker_variant.database import get_sneaker_variant_repository_factory
from repositories.sneaker_variant import SneakerVariantRepository
from services.sneaker_variant import SneakerVariantService


def get_sneaker_variant_service_factory(
        sneaker_variant_repository_factory: Callable[[], SneakerVariantRepository] = Depends(
            get_sneaker_variant_repository_factory
        ),
) -> Callable[[], SneakerVariantService]:
    return lambda: SneakerVariantService(sneaker_variant_repository_factory)
