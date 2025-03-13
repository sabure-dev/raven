from typing import Callable

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.session.database import get_async_session
from repositories.users import UserRepository


def get_user_repository(session: AsyncSession = Depends(get_async_session)) -> UserRepository:
    return UserRepository(session)


def get_user_repository_factory(session: AsyncSession = Depends(get_async_session)) -> Callable[[], UserRepository]:
    return lambda: UserRepository(session)
