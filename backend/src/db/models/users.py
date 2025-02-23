from datetime import datetime

from pydantic import EmailStr
from sqlalchemy import String, DateTime, func, Float, CheckConstraint
from sqlalchemy.orm import mapped_column, Mapped

from db.session.base import Base


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str] = mapped_column(String(25), index=True, unique=True)
    email: Mapped[EmailStr] = mapped_column(String(100), index=True, unique=True)
    password: Mapped[str] = mapped_column(String(100))
    balance: Mapped[float] = mapped_column(Float(precision=4), CheckConstraint('balance >= 0'))

    is_superuser: Mapped[bool] = mapped_column(default=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_verified: Mapped[bool] = mapped_column(default=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
