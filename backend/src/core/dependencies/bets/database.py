from typing import Callable

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.session.database import get_async_session
from repositories.bets import BetRepository


def get_bet_repository_factory(
        session: AsyncSession = Depends(get_async_session),
) -> Callable[[], BetRepository]:
    return lambda: BetRepository(session)
