from datetime import datetime

from sqlalchemy import ForeignKey, DateTime, func, Enum, CheckConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship

from db.session.base import Base
from schemas.orders.orders import OrderStatus, OrderOut, OrderItemOut


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    order_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), default=OrderStatus.PENDING)
    total_amount: Mapped[float] = mapped_column(default=0.0)

    user: Mapped["User"] = relationship("User", back_populates="orders", lazy="raise")
    items: Mapped[list["OrderItem"]] = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan",
        lazy="raise"
    )

    __table_args__ = (
        CheckConstraint("total_amount >= 0", name="check_order_total_amount"),
    )

    def to_read_model(self, include_items: bool = False) -> OrderOut:
        return OrderOut(
            id=self.id,
            user_id=self.user_id,
            order_date=self.order_date,
            items=[item.to_read_model(include_sneaker_variant=True) for item in
                   self.items] if include_items and self.items is not None else None,
            status=self.status,
            total_amount=self.total_amount,
        )


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"))
    quantity: Mapped[int] = mapped_column(default=1)
    price_at_time: Mapped[float] = mapped_column(default=0.0)
    sneaker_variant_id: Mapped[int] = mapped_column(ForeignKey("sneaker_variants.id", ondelete="RESTRICT"))

    sneaker_variant: Mapped["SneakerVariant"] = relationship("SneakerVariant", lazy="raise")
    order: Mapped["Order"] = relationship("Order", back_populates="items", lazy="raise")

    __table_args__ = (
        CheckConstraint("quantity > 0", name="check_order_item_quantity"),
        CheckConstraint("price_at_time >= 0", name="check_order_item_price"),
    )

    def to_read_model(self, include_sneaker_variant: bool = False) -> OrderItemOut:
        return OrderItemOut(
            id=self.id,
            order_id=self.order_id,
            quantity=self.quantity,
            sneaker_variant_id=self.sneaker_variant_id,
            price_at_time=self.price_at_time,
            sneaker_variant=self.sneaker_variant.to_read_model_with_name() if include_sneaker_variant and self.sneaker_variant is not None else None,
        )
