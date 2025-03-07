from typing import Callable

from schemas.use_cases import VerifyEmailInput
from services.jwt import TokenService
from services.users import UserService
from use_cases.base import BaseUseCase


class VerifyEmailUseCase(BaseUseCase[VerifyEmailInput, None]):
    def __init__(
            self,
            user_service_factory: Callable[[], UserService],
            token_service_factory: Callable[[], TokenService]
    ):
        self.user_service = user_service_factory()
        self.token_service = token_service_factory()

    async def execute(self, input_data: VerifyEmailInput) -> None:
        payload = self.token_service.verify_token(input_data.token)
        username = payload.get('sub')

        user = await self.user_service.get_user_by_username(username)

        await self.user_service.update_user_verification(user, True)
