from typing import Callable

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.session.database import get_async_session
from repositories.order import OrderRepository
from repositories.order_item import OrderItemRepository


def get_order_repository_factory(
        session: AsyncSession = Depends(get_async_session),
) -> Callable[[], OrderRepository]:
    return lambda: OrderRepository(session)


def get_order_item_repository_factory(
        session: AsyncSession = Depends(get_async_session),
) -> Callable[[], OrderItemRepository]:
    return lambda: OrderItemRepository(session)
