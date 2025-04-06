from typing import Callable, Literal

from sqlalchemy import or_, and_
from sqlalchemy.orm import selectinload

from core.utils.repository import AbstractRepository
from db.models import SneakerVariant, SneakerModel
from db.models.orders import Order, OrderItem
from schemas.orders.orders import OrderCreate


class OrderService:
    def __init__(self, order_repo_factory: Callable[[], AbstractRepository]):
        self._order_repo = order_repo_factory()

    async def create_order(self, order: OrderCreate, user_id: int) -> Order:
        order_dict = order.model_dump()
        order_dict['user_id'] = user_id
        order = await self._order_repo.create_one(order_dict)
        return order

    async def get_user_orders(
            self,
            user_id: int,
            order_id: int | None = None,
            sneaker_name: str | None = None,
            sneaker_brand: str | None = None,
            search_query: str | None = None,
            offset: int | None = None,
            limit: int | None = None,
            sort_by_date: Literal["asc", "desc"] | None = None
    ) -> list[Order]:
        filters = [Order.user_id == user_id]
        options = [selectinload(Order.items).joinedload(OrderItem.sneaker_variant).joinedload(SneakerVariant.model)]
        order_by = ("order_date", sort_by_date) if sort_by_date else None

        order_item_filters = []
        sneaker_variant_filters = []
        sneaker_model_filters = []
        joins = {}

        if order_id:
            filters.append(Order.id == order_id)

        if sneaker_name:
            sneaker_model_filters.append(SneakerModel.name == sneaker_name)

        if sneaker_brand:
            sneaker_model_filters.append(SneakerModel.brand == sneaker_brand)

        if search_query:
            search_pattern = f"%{search_query}%"
            sneaker_model_filters.append(
                or_(
                    SneakerModel.name.ilike(search_pattern),
                    SneakerModel.description.ilike(search_pattern)
                )
            )

        if sneaker_model_filters:
            sneaker_variant_filters.append(SneakerVariant.model.has(and_(*sneaker_model_filters)))
        if sneaker_variant_filters:
            order_item_filters.append(OrderItem.sneaker_variant.has(and_(*sneaker_variant_filters)))
        if order_item_filters:
            joins["items"] = and_(*order_item_filters)

        orders = await self._order_repo.find_all_with_filters(
            filters=filters,
            joins=joins,
            order_by=order_by,
            options=options,
            offset=offset,
            limit=limit
        )

        return orders

    async def cancel_order(self):
        pass
