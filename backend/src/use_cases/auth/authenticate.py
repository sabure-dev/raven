from typing import Callable

from fastapi.security import OAuth2PasswordRequestForm

from schemas.auth.auth import LoginRequest, TokenResponse
from services.auth import AuthService
from use_cases.base import BaseUseCase


class AuthenticateUserUseCase(BaseUseCase[OAuth2PasswordRequestForm, TokenResponse]):
    def __init__(self, auth_service_factory: Callable[[], AuthService]):
        self.auth_service = auth_service_factory()

    async def execute(self, form_data: OAuth2PasswordRequestForm) -> TokenResponse:
        input_data = LoginRequest(
            username=form_data.username,
            password=form_data.password,
        )
        return await self.auth_service.authenticate_user(input_data)
