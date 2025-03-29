from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import ForeignKey, DateTime, func, Enum, Float, CheckConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship

from db.session.base import Base


class OrderStatus(PyEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    order_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), default=OrderStatus.PENDING)
    total_amount: Mapped[float] = mapped_column(Float(precision=4), default=0.0)

    user: Mapped["User"] = relationship(back_populates="orders")
    items: Mapped[list["OrderItem"]] = relationship(
        back_populates="orders",
        cascade="all, delete-orphan",
        lazy="raise"
    )

    __table_args__ = (
        CheckConstraint("total_amount >= 0", name="check_order_total_amount"),
    )


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"))
    quantity: Mapped[int] = mapped_column(default=1)
    price_at_time: Mapped[float] = mapped_column(Float(precision=10), default=0.0)

    order: Mapped["Order"] = relationship(back_populates="items")
    variant: Mapped["SneakerVariant"] = relationship()

    __table_args__ = (
        CheckConstraint("quantity > 0", name="check_order_item_quantity"),
        CheckConstraint("price_at_time >= 0", name="check_order_item_price"),
    )
