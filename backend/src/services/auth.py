from typing import Callable

from core.exceptions import InvalidCredentialsException, InactiveUserException, UnverifiedEmailException, \
    TokenExpiredException
from core.utils.password import verify_password
from core.utils.repository import AbstractRepository
from schemas.auth import LoginRequest, TokenResponse
from services.jwt import TokenService


class AuthService:
    def __init__(
        self,
        user_repo_factory: Callable[[], AbstractRepository],
        token_service_factory: Callable[[], TokenService]
    ):
        self.user_repo = user_repo_factory()
        self.token_service = token_service_factory()

    async def authenticate_user(self, credentials: LoginRequest) -> TokenResponse:
        user = await self.user_repo.find_one_by_field("username", credentials.username)

        if not user or not self._verify_password(credentials.password, user.password):
            raise InvalidCredentialsException()
        if not user.is_active:
            raise InactiveUserException()
        if not user.is_verified:
            raise UnverifiedEmailException()

        return self.token_service.create_tokens(user)

    async def refresh_token(self, refresh_token: str) -> TokenResponse:
        try:
            payload = self.token_service.verify_token(refresh_token)
            user = await self.user_repo.find_one_by_field("username", payload["sub"])
            if not user:
                raise InvalidCredentialsException()
            if not user.is_active:
                raise InactiveUserException()
            if not user.is_verified:
                raise UnverifiedEmailException()

            return self.token_service.create_tokens(user)

        except TokenExpiredException:
            raise
        except InvalidCredentialsException:
            raise
        except Exception:
            raise InvalidCredentialsException()

    @staticmethod
    def _verify_password(plain_password: str, hashed_password: str) -> bool:
        return verify_password(plain_password, hashed_password)
