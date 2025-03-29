from datetime import datetime

from pydantic import EmailStr
from sqlalchemy import String, DateTime, func, Float, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship

from db.session.base import Base
from schemas.users.users import UserOut


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str] = mapped_column(String(25), index=True)
    email: Mapped[EmailStr] = mapped_column(String(100), index=True)
    password: Mapped[str] = mapped_column(String(100))
    balance: Mapped[float] = mapped_column(Float(precision=4), default=0.0)

    orders: Mapped[list["Order"]] = relationship(
        "Order",
        back_populates="user",
        lazy="raise",
        cascade="all, delete-orphan"
    )

    is_superuser: Mapped[bool] = mapped_column(default=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_verified: Mapped[bool] = mapped_column(default=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    __table_args__ = (
        UniqueConstraint("username", name="uq_users_username"),
        UniqueConstraint("email", name="uq_users_email"),
        CheckConstraint("balance >= 0", name="check_users_balance"),
    )

    def to_read_model(self) -> UserOut:
        return UserOut(
            id=self.id,
            username=self.username,
            email=self.email,
            balance=self.balance,
            is_superuser=self.is_superuser,
            is_active=self.is_active,
            is_verified=self.is_verified,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
