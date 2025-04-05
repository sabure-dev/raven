from typing import Callable

from fastapi import Depends

from core.dependencies.orders.services import get_order_service_factory, get_order_item_service_factory
from core.dependencies.sneaker_variant.services import get_sneaker_variant_service_factory
from services.order_items import OrderItemService
from services.orders import OrderService
from services.sneaker_variant import SneakerVariantService
from use_cases.orders.create_order import CreateOrderUseCase


def get_create_order_use_case(
        order_service_factory: Callable[[], OrderService] = Depends(
            get_order_service_factory
        ),
        order_item_service_factory: Callable[[], OrderItemService] = Depends(
            get_order_item_service_factory
        ),
        sneaker_variant_service_factory: Callable[[], SneakerVariantService] = Depends(
            get_sneaker_variant_service_factory
        )
) -> CreateOrderUseCase:
    return CreateOrderUseCase(order_service_factory, order_item_service_factory, sneaker_variant_service_factory)
