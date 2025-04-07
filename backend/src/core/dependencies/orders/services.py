from typing import Callable

from fastapi import Depends

from core.dependencies.orders.database import (
    get_order_repository_factory, get_order_item_repository_factory,
)
from repositories.order import OrderRepository
from services.order_items import OrderItemService
from services.orders import OrderService


def get_order_service_factory(
        order_repository_factory: Callable[[], OrderRepository] = Depends(
            get_order_repository_factory
        ),
) -> Callable[[], OrderService]:
    return lambda: OrderService(order_repository_factory)


def get_order_item_service_factory(
        order_item_repository_factory: Callable[[], OrderRepository] = Depends(
            get_order_item_repository_factory
        ),
) -> Callable[[], OrderItemService]:
    return lambda: OrderItemService(order_item_repository_factory)
