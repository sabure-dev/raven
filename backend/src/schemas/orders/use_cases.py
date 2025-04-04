from pydantic import BaseModel

from schemas.orders.orders import OrderCreate, OrderItemCreate


class BaseModelWithConfig(BaseModel):
    model_config = {
        "arbitrary_types_allowed": True,
    }


class CreateOrderInput(BaseModelWithConfig):
    order: OrderCreate
    items: list[OrderItemCreate]
