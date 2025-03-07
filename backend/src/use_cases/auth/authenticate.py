from typing import Callable

from schemas.auth import LoginRequest, TokenResponse
from services.auth import AuthService
from use_cases.base import BaseUseCase


class AuthenticateUserUseCase(BaseUseCase[LoginRequest, TokenResponse]):
    def __init__(self, auth_service_factory: Callable[[], AuthService]):
        self.auth_service = auth_service_factory()

    async def execute(self, input_data: LoginRequest) -> TokenResponse:
        return await self.auth_service.authenticate_user(input_data)
