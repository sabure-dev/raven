from typing import Annotated

from fastapi import BackgroundTasks
from pydantic import BaseModel, EmailStr, Field

from schemas.users import UserCreate


class BaseModelWithConfig(BaseModel):
    model_config = {
        "arbitrary_types_allowed": True,
    }


class CreateUserInput(BaseModelWithConfig):
    user: UserCreate
    background_tasks: Annotated[BackgroundTasks, Field(exclude=True)]


class VerifyEmailInput(BaseModelWithConfig):
    token: str


class GetUserInput(BaseModelWithConfig):
    user_id: int


class DeleteUserInput(BaseModelWithConfig):
    user_id: int


class UpdateUserEmailInput(BaseModelWithConfig):
    user_id: int
    new_email: EmailStr
    background_tasks: Annotated[BackgroundTasks, Field(exclude=True)]


class UpdateUserUsernameInput(BaseModelWithConfig):
    user_id: int
    new_username: str


class RequestPasswordResetInput(BaseModelWithConfig):
    email: EmailStr
    background_tasks: Annotated[BackgroundTasks, Field(exclude=True)]


class UpdatePasswordInput(BaseModelWithConfig):
    token: str
    new_password: str


class ChangePasswordInput(BaseModelWithConfig):
    user_id: int
    current_password: str
    new_password: str
