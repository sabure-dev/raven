from typing import Callable

from core.utils.repository import AbstractRepository
from db.models.orders import Order
from schemas.orders.orders import OrderCreate


class OrderService:
    def __init__(self, order_repo_factory: Callable[[], AbstractRepository]):
        self.order_repo = order_repo_factory()

    async def create_order(self, order: OrderCreate) -> Order:
        order_dict = order.model_dump()
        order = await self.order_repo.create_one(order_dict)
        return order

    async def cancel_order(self):
        pass

    async def get_user_orders(self):
        pass
