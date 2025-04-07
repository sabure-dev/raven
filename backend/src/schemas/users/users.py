from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from schemas.orders.orders import OrderOut


class UserBase(BaseModel):
    username: str = Field(..., min_length=3)
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserOut(UserBase):
    id: int
    balance: float

    is_superuser: bool
    is_active: bool
    is_verified: bool

    created_at: datetime
    updated_at: datetime

    orders: list[OrderOut] | None = None


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8)
