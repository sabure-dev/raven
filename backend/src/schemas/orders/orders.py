from datetime import datetime
from enum import Enum as PyEnum

from pydantic import BaseModel, Field

from schemas.sneaker_variant.sneaker_variant import SneakerVariantOut


class OrderStatus(PyEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class OrderItemBase(BaseModel):
    quantity: int = Field(..., gt=0)
    sneaker_variant_id: int
    price_at_time: float | None = Field(None, ge=0)
    order_id: int | None = None


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemOut(OrderItemBase):
    id: int
    sneaker_variant: SneakerVariantOut | None


class OrderBase(BaseModel):
    total_amount: float | None = Field(None, ge=0)


class OrderCreate(OrderBase):
    pass


class OrderOut(OrderBase):
    id: int
    user_id: int
    items: list[OrderItemOut] | None = None
    order_date: datetime
    status: OrderStatus
