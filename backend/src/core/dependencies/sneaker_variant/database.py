from typing import Callable

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.session.database import get_async_session
from repositories.sneaker_variant import SneakerVariantRepository


def get_sneaker_variant_repository_factory(
        session: AsyncSession = Depends(get_async_session),
) -> Callable[[], SneakerVariantRepository]:
    return lambda: SneakerVariantRepository(session)
