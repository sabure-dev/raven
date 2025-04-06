from typing import Callable

from core.exceptions import ItemNotFoundException
from schemas.orders.orders import OrderOut, OrderCreate, OrderItemCreateInDB
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
        order_items = []

        variant_ids = [item.sneaker_variant_id for item in input_data.items]
        variant_map = await self.sneaker_variant_service.get_all_by_ids(variant_ids)

        for item in input_data.items:
            variant = variant_map.get(item.sneaker_variant_id, None)
            if not variant:
                raise ItemNotFoundException("SneakerVariant", "id", str(item.sneaker_variant_id))
            order_items.append(OrderItemCreateInDB(
                quantity=item.quantity,
                sneaker_variant_id=item.sneaker_variant_id,
                price_at_time=variant.model.price,
            ))
            total_amount += variant.model.price * item.quantity

        order = await self.order_service.create_order(
            OrderCreate(total_amount=total_amount),
            input_data.user_id
        )

        for item in order_items:
            item.order_id = order.id
            await self.order_item_service.create_order_item(item)
            await self.sneaker_variant_service.update_quantity_by_delta(item.sneaker_variant_id, -item.quantity)
        return order.to_read_model()
