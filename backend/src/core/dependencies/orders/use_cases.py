from typing import Callable

from fastapi import Depends

from core.dependencies.orders.services import get_order_service_factory, get_order_item_service_factory
from core.dependencies.sneaker_variant.services import get_sneaker_variant_service_factory
from core.dependencies.users.services import get_user_service_factory
from services.order_items import OrderItemService
from services.orders import OrderService
from services.sneaker_variant import SneakerVariantService
from services.users import UserService
from use_cases.orders.cancel_order import CancelOrderUseCase
from use_cases.orders.create_order import CreateOrderUseCase
from use_cases.orders.get_orders import GetOrdersUseCase


def get_create_order_use_case(
        order_service_factory: Callable[[], OrderService] = Depends(
            get_order_service_factory
        ),
        order_item_service_factory: Callable[[], OrderItemService] = Depends(
            get_order_item_service_factory
        ),
        sneaker_variant_service_factory: Callable[[], SneakerVariantService] = Depends(
            get_sneaker_variant_service_factory
        ),
        user_service_factory: Callable[[], UserService] = Depends(
            get_user_service_factory
        )
) -> CreateOrderUseCase:
    return CreateOrderUseCase(
        order_service_factory,
        order_item_service_factory,
        sneaker_variant_service_factory,
        user_service_factory
    )


def get_get_orders_use_case(
        order_service_factory: Callable[[], OrderService] = Depends(
            get_order_service_factory
        ),
) -> GetOrdersUseCase:
    return GetOrdersUseCase(order_service_factory)


def get_cancel_order_use_case(
        order_service_factory: Callable[[], OrderService] = Depends(
            get_order_service_factory
        ),
        user_service_factory: Callable[[], UserService] = Depends(
            get_user_service_factory
        ),
) -> CancelOrderUseCase:
    return CancelOrderUseCase(order_service_factory, user_service_factory)
