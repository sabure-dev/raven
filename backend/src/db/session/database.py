from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from core.config.config import settings

engine = create_async_engine(
    f"postgresql+asyncpg://\
{settings.db_settings.DB_USER}:\
{settings.db_settings.DB_PASSWORD}@\
{settings.db_settings.DB_HOST}:\
{settings.db_settings.DB_PORT}/\
{settings.db_settings.DB_NAME}"
)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session():
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()
