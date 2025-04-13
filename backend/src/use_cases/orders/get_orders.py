from typing import Callable

from schemas.orders.orders import OrderOut
from schemas.orders.use_cases import GetOrdersInput
from services.orders import OrderService
from use_cases.base import BaseUseCase


class GetOrdersUseCase(BaseUseCase[GetOrdersInput, list[OrderOut]]):
    def __init__(
            self, order_service_factory: Callable[[], OrderService]
    ):
        self.order_service = order_service_factory()

    async def execute(
            self, input_data: GetOrdersInput
    ) -> list[OrderOut]:
        orders = await self.order_service.get_user_orders(
            user_id=input_data.user_id,
            order_id=input_data.params.order_id,
            sneaker_name=input_data.params.sneaker_name,
            sneaker_brand=input_data.params.sneaker_brand,
            search_query=input_data.params.search_query,
            offset=input_data.params.offset,
            limit=input_data.params.limit,
            sort_by_date=input_data.params.sort_by_date,
        )
        return [order.to_read_model(include_items=True) for order in orders]
