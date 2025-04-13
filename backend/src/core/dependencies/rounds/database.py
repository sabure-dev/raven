from typing import Callable

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.session.database import get_async_session
from repositories.rounds import RoundRepository


def get_round_repository_factory(
        session: AsyncSession = Depends(get_async_session),
) -> Callable[[], RoundRepository]:
    return lambda: RoundRepository(session)
