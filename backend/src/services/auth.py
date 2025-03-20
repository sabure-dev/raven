from typing import Callable

from core.exceptions import InvalidCredentialsException, InactiveUserException, UnverifiedEmailException
from core.utils.password import verify_password
from schemas.auth import LoginRequest, TokenResponse
from services.jwt import TokenService
from services.users import UserService


class AuthService:
    def __init__(
            self,
            user_service_factory: Callable[[], UserService],
            token_service_factory: Callable[[], TokenService]
    ):
        self.user_service = user_service_factory()
        self.token_service = token_service_factory()

    async def authenticate_user(self, credentials: LoginRequest) -> TokenResponse:
        user = await self.user_service.get_user_by_username(credentials.username)

        if not self._verify_password(credentials.password, user.password):
            raise InvalidCredentialsException()
        if not user.is_active:
            raise InactiveUserException()
        if not user.is_verified:
            raise UnverifiedEmailException()

        return await self.token_service.create_tokens(user)

    async def refresh_token(self, refresh_token: str) -> TokenResponse:
        payload = await self.token_service.verify_token(refresh_token)
        username = await self.token_service.get_username_from_token_payload(payload)
        user = await self.user_service.get_user_by_username(username)
        if not user.is_active:
            raise InactiveUserException()
        if not user.is_verified:
            raise UnverifiedEmailException()

        return await self.token_service.create_tokens(user)

    @staticmethod
    def _verify_password(plain_password: str, hashed_password: str) -> bool:
        return verify_password(plain_password, hashed_password)
