from typing import Callable

from schemas.auth import TokenResponse, RefreshTokenRequest
from services.auth import AuthService
from use_cases.base import BaseUseCase


class RefreshTokenUseCase(BaseUseCase[RefreshTokenRequest, TokenResponse]):
    def __init__(self, auth_service_factory: Callable[[], AuthService]):
        self.auth_service = auth_service_factory()

    async def execute(self, input_data: RefreshTokenRequest) -> TokenResponse:
        return await self.auth_service.refresh_token(input_data.refresh_token)
