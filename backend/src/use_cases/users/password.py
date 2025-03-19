from typing import Callable

from fastapi import BackgroundTasks

from schemas.use_cases import RequestPasswordResetInput, UpdatePasswordInput, ChangePasswordInput
from services.email import EmailService
from services.jwt import TokenService
from services.users import UserService
from use_cases.base import BaseUseCase


class RequestPasswordResetUseCase(BaseUseCase[RequestPasswordResetInput, None]):
    def __init__(
            self,
            user_service_factory: Callable[[], UserService],
            token_service_factory: Callable[[], TokenService],
            email_service_factory: Callable[[], EmailService],
            background_tasks: BackgroundTasks
    ):
        self.user_service = user_service_factory()
        self.token_service = token_service_factory()
        self.email_service = email_service_factory()
        self.background_tasks = background_tasks

    async def execute(self, input_data: RequestPasswordResetInput) -> None:
        user = await self.user_service.get_verified_user_by_email(input_data.email)

        token = await self.token_service.create_verification_token(user)

        self.background_tasks.add_task(
            self.email_service.send_change_password_email,
            input_data.email,
            token
        )


class UpdatePasswordUseCase(BaseUseCase[UpdatePasswordInput, None]):
    def __init__(
            self,
            user_service_factory: Callable[[], UserService],
            token_service_factory: Callable[[], TokenService]
    ):
        self.user_service = user_service_factory()
        self.token_service = token_service_factory()

    async def execute(self, input_data: UpdatePasswordInput) -> None:
        payload = await self.token_service.verify_token(input_data.token)
        username = await self.token_service.get_username_from_token_payload(payload)

        user = await self.user_service.get_verified_user_by_email(username)

        await self.user_service.update_user_password(user, input_data.new_password)


class ChangePasswordUseCase(BaseUseCase[ChangePasswordInput, None]):
    def __init__(
            self,
            user_service_factory: Callable[[], UserService]
    ):
        self.user_service = user_service_factory()

    async def execute(self, input_data: ChangePasswordInput) -> None:
        await self.user_service.change_password(
            input_data.user_id,
            input_data.current_password,
            input_data.new_password
        )
