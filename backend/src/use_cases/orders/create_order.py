from typing import Callable

from schemas.orders.orders import OrderOut
from schemas.orders.use_cases import CreateOrderInput
from services.order_items import OrderItemService
from services.orders import OrderService
from use_cases.base import BaseUseCase


class CreateOrderUseCase(BaseUseCase[CreateOrderInput, OrderOut]):
    def __init__(
            self,
            order_service_factory: Callable[[], OrderService],
            order_item_service_factory: Callable[[], OrderItemService],
    ):
        self.order_service = order_service_factory()
        self.order_item_service = order_item_service_factory()

    async def execute(self, input_data: CreateOrderInput) -> OrderOut:
        order = await self.order_service.create_order(
            input_data.order
        )
        for item in input_data.items:
            item.order_id = order.id
            await self.order_item_service.create_order_item(item)
        return order.to_read_model()
