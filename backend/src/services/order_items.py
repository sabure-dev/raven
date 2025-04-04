from typing import Callable

from core.utils.repository import AbstractRepository
from db.models.orders import OrderItem
from schemas.orders.orders import OrderItemCreate


class OrderItemService:
    def __init__(self, order_item_repo_factory: Callable[[], AbstractRepository]):
        self.order_item_repo = order_item_repo_factory()

    async def create_order_item(self, order_item: OrderItemCreate) -> OrderItem:
        order_item_dict = order_item.model_dump()
        order_item = await self.order_item_repo.create_one(order_item_dict)
        return order_item
