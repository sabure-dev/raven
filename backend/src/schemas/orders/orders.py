from datetime import datetime
from enum import Enum as PyEnum

from pydantic import BaseModel, Field, field_validator


class OrderStatus(PyEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class OrderItemBase(BaseModel):
    quantity: int = Field(..., gt=0)
    price_at_time: float = Field(..., ge=0)
    order_id: int


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemOut(OrderItemBase):
    id: int


class OrderBase(BaseModel):
    user_id: int
    total_amount: float = Field(..., ge=0)


class OrderCreate(OrderBase):
    @field_validator('total_amount')
    def validate_total(cls, v, values):
        if 'items' in values and v != sum(item.price_at_time * item.quantity for item in values['items']):
            raise ValueError("Total amount must match sum of items")
        return v


class OrderOut(OrderBase):
    id: int
    items: list[OrderItemOut]
    order_date: datetime
    status: OrderStatus
