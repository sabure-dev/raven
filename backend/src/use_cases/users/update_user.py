from typing import Callable

from schemas.use_cases import UpdateUserEmailInput, UpdateUserUsernameInput
from schemas.users import UserOut
from services.email import EmailService
from services.jwt import TokenService
from services.users import UserService
from use_cases.base import BaseUseCase


class UpdateUserEmailUseCase(BaseUseCase[UpdateUserEmailInput, UserOut]):
    def __init__(
            self,
            user_service_factory: Callable[[], UserService],
            token_service_factory: Callable[[], TokenService],
            email_service_factory: Callable[[], EmailService]
    ):
        self.user_service = user_service_factory()
        self.token_service = token_service_factory()
        self.email_service = email_service_factory()

    async def execute(self, input_data: UpdateUserEmailInput) -> UserOut:
        updated_user = await self.user_service.update_user_email(
            input_data.user_id,
            input_data.new_email
        )

        token = self.token_service.create_verification_token(updated_user)

        input_data.background_tasks.add_task(
            self.email_service.send_verification_email,
            input_data.new_email,
            token
        )

        return updated_user.to_read_model()


class UpdateUserUsernameUseCase(BaseUseCase[UpdateUserUsernameInput, UserOut]):
    def __init__(self, user_service_factory: Callable[[], UserService]):
        self.user_service = user_service_factory()

    async def execute(self, input_data: UpdateUserUsernameInput) -> UserOut:
        return await self.user_service.update_user_username(
            input_data.user_id,
            input_data.new_username
        )
