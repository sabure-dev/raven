from typing import Callable

from schemas.orders.orders import OrderOut
from schemas.orders.use_cases import CancelOrderInput
from services.orders import OrderService
from services.users import UserService
from use_cases.base import BaseUseCase


class CancelOrderUseCase(BaseUseCase[CancelOrderInput, OrderOut]):
    def __init__(
            self,
            order_service_factory: Callable[[], OrderService],
            user_service_factory: Callable[[], UserService]
    ):
        self.order_service = order_service_factory()
        self.user_service = user_service_factory()

    async def execute(self, input_data: CancelOrderInput) -> OrderOut:
        updated_order = await self.order_service.cancel_order(input_data.order_id, input_data.user_id)
        await self.user_service.update_balance_after_order(input_data.user_id, -updated_order.total_amount)
        return updated_order.to_read_model()
