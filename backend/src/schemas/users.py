from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int
    balance: float

    is_superuser: bool
    is_active: bool
    is_verified: bool

    created_at: datetime
    updated_at: datetime
