from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from core.config.config import settings


class DatabaseHelper:
    def __init__(self, url, echo, pool_size, max_overflow):
        self.engine = create_async_engine(
            url=url,
            echo=echo,
            pool_size=pool_size,
            max_overflow=max_overflow,
        )
        self.async_session_maker = async_sessionmaker(
            self.engine,
            expire_on_commit=False,
            autoflush=False,
        )

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.async_session_maker() as session:
            try:
                async with session.begin():
                    yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()


db_helper = DatabaseHelper(
    url=f"postgresql+asyncpg://"
        f"{settings.db_settings.DB_USER}:"
        f"{settings.db_settings.DB_PASSWORD}@"
        f"{settings.db_settings.DB_HOST}:"
        f"{settings.db_settings.DB_PORT}/"
        f"{settings.db_settings.DB_NAME}",
    echo=False,
    pool_size=20,
    max_overflow=10,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with db_helper.get_session() as session:
        yield session
