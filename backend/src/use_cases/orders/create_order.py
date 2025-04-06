from typing import Callable

from core.exceptions import ItemNotFoundException
from schemas.orders.orders import OrderOut
from schemas.orders.use_cases import CreateOrderInput
from services.order_items import OrderItemService
from services.orders import OrderService
from services.sneaker_variant import SneakerVariantService
from use_cases.base import BaseUseCase


class CreateOrderUseCase(BaseUseCase[CreateOrderInput, OrderOut]):
    def __init__(
            self,
            order_service_factory: Callable[[], OrderService],
            order_item_service_factory: Callable[[], OrderItemService],
            sneaker_variant_service_factory: Callable[[], SneakerVariantService],
    ):
        self.order_service = order_service_factory()
        self.order_item_service = order_item_service_factory()
        self.sneaker_variant_service = sneaker_variant_service_factory()

    async def execute(self, input_data: CreateOrderInput) -> OrderOut:
        total_amount = 0

        variant_ids = [item.sneaker_variant_id for item in input_data.items]
        variant_map = await self.sneaker_variant_service.get_all_by_ids(variant_ids)

        for item in input_data.items:
            variant = variant_map.get(item.sneaker_variant_id, None)
            if not variant:
                raise ItemNotFoundException("SneakerVariant", "id", str(item.sneaker_variant_id))
            item.price_at_time = variant.model.price
            total_amount += item.price_at_time * item.quantity

        input_data.order.total_amount = total_amount
        order = await self.order_service.create_order(
            input_data.order,
            input_data.user_id
        )

        for item in input_data.items:
            item.order_id = order.id
            await self.order_item_service.create_order_item(item)
        return order.to_read_model()
