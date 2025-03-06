from typing import Callable

from core.exceptions import UnverifiedEmailException
from schemas.use_cases import RequestPasswordResetInput, UpdatePasswordInput
from services.email import EmailService
from services.jwt import TokenService
from services.users import UserService
from use_cases.base import BaseUseCase


class RequestPasswordResetUseCase(BaseUseCase[RequestPasswordResetInput, None]):
    def __init__(
            self,
            user_service_factory: Callable[[], UserService],
            token_service_factory: Callable[[], TokenService],
            email_service_factory: Callable[[], EmailService]
    ):
        self.user_service = user_service_factory()
        self.token_service = token_service_factory()
        self.email_service = email_service_factory()

    async def execute(self, input_data: RequestPasswordResetInput) -> None:
        user = await self.user_service.get_user_by_email(input_data.email)

        if not user.is_verified:
            raise UnverifiedEmailException()

        token = self.token_service.create_verification_token(user)

        input_data.background_tasks.add_task(
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
        payload = self.token_service.verify_token(input_data.token)
        username = payload.get('sub')

        user = await self.user_service.get_user_by_username(username)

        if not user.is_verified:
            raise UnverifiedEmailException()

        await self.user_service.update_user_password(user, input_data.new_password)
