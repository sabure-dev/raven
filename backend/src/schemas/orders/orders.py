from datetime import datetime
from enum import Enum as PyEnum
from typing import Literal

from pydantic import BaseModel, Field

from schemas.sneaker_variant.sneaker_variant import SneakerVariantOut, SneakerVariantOutWithModel


class OrderStatus(PyEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class OrderItemBase(BaseModel):
    quantity: int = Field(..., gt=0)
    sneaker_variant_id: int


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemCreateInDB(OrderItemBase):
    price_at_time: float | None = Field(None, ge=0)
    order_id: int | None = None


class OrderItemOut(OrderItemBase):
    id: int
    price_at_time: float | None = Field(None, ge=0)
    order_id: int | None = None
    sneaker_variant: SneakerVariantOutWithModel | None


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


class OrderParams(BaseModel):
    order_id: int | None = None
    sneaker_name: str | None = None
    sneaker_brand: str | None = None
    search_query: str | None = None
    offset: int | None = None
    limit: int | None = None
    sort_by_date: Literal["asc", "desc"] | None = None
