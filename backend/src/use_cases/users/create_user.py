from typing import Callable

from schemas.use_cases import CreateUserInput
from services.email import EmailService
from services.jwt import TokenService
from services.users import UserService
from use_cases.base import BaseUseCase


class CreateUserUseCase(BaseUseCase[CreateUserInput, int]):
    def __init__(
            self,
            user_service_factory: Callable[[], UserService],
            token_service_factory: Callable[[], TokenService],
            email_service_factory: Callable[[], EmailService]
    ):
        self.user_service = user_service_factory()
        self.token_service = token_service_factory()
        self.email_service = email_service_factory()

    async def execute(self, input_data: CreateUserInput) -> int:
        user_id, user = await self.user_service.create_user(input_data.user)

        token = self.token_service.create_verification_token(user)

        input_data.background_tasks.add_task(
            self.email_service.send_verification_email,
            input_data.user.email,
            token
        )

        return user_id
