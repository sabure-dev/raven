from typing import Callable

from fastapi.security import OAuth2PasswordBearer

from core.exceptions import InvalidCredentialsException, InactiveUserException, \
    UnverifiedEmailException, InsufficientPermissionsException
from db.models.users import User
from services.jwt import TokenService
from services.users import UserService


class SecurityService:
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

    def __init__(
            self,
            user_service_factory: Callable[[], UserService],
            token_service_factory: Callable[[], TokenService]
    ):
        self.user_service = user_service_factory()
        self.token_service = token_service_factory()

    async def get_current_user(self, token: str) -> User:
        payload = await self.token_service.verify_token(token)
        username = await self.token_service.get_username_from_token_payload(payload)

        if not username:
            raise InvalidCredentialsException()

        user = await self.user_service.get_user_by_username(username)

        if not user.is_active:
            raise InactiveUserException()

        return user

    async def get_current_active_verified_user(self, current_user: User) -> User:
        if not current_user.is_verified:
            raise UnverifiedEmailException()
        return current_user

    async def get_current_superuser(self, current_user: User) -> User:
        if not current_user.is_superuser:
            raise InsufficientPermissionsException()
        return current_user
