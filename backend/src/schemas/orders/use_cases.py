from pydantic import BaseModel

from schemas.orders.orders import OrderItemCreate, OrderParams


class BaseModelWithConfig(BaseModel):
    model_config = {
        "arbitrary_types_allowed": True,
    }


class CreateOrderInput(BaseModelWithConfig):
    items: list[OrderItemCreate]
    user_id: int


class GetOrdersInput(BaseModelWithConfig):
    user_id: int
    params: OrderParams
