from typing import Callable

from sqlalchemy.exc import IntegrityError

from core.exceptions import ItemNotFoundException
from core.utils.repository import AbstractRepository
from db.models.orders import OrderItem
from schemas.orders.orders import OrderItemCreateInDB


class OrderItemService:
    def __init__(self, order_item_repo_factory: Callable[[], AbstractRepository]):
        self.order_item_repo = order_item_repo_factory()

    async def _handle_foreign_key_violation(
            self, field: str, value: str,
    ):
        raise ItemNotFoundException("SneakerVariant", field, value)

    async def create_order_item(self, order_item: OrderItemCreateInDB) -> OrderItem:
        order_item_dict = order_item.model_dump()
        try:
            order_item = await self.order_item_repo.create_one(order_item_dict)
            return order_item
        except IntegrityError as e:
            if "foreign key" in str(e).lower():
                await self._handle_foreign_key_violation("id", str(order_item.sneaker_variant_id))
