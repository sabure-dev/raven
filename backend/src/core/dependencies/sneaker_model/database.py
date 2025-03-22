from typing import Callable

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.session.database import get_async_session
from repositories.sneakers import SneakerModelRepository


def get_sneaker_model_repository_factory(
        session: AsyncSession = Depends(get_async_session),
) -> Callable[[], SneakerModelRepository]:
    return lambda: SneakerModelRepository(session)
