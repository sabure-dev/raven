from typing import Callable

from fastapi import Depends

from core.dependencies.jwt.services import get_token_service_factory
from core.dependencies.users.services import get_user_service_factory
from services.auth import AuthService
from services.jwt import TokenService
from services.users import UserService


def get_auth_service_factory(
        user_service_factory: Callable[[], UserService] = Depends(get_user_service_factory),
        token_service_factory: Callable[[], TokenService] = Depends(get_token_service_factory)
) -> Callable[[], AuthService]:
    return lambda: AuthService(user_service_factory, token_service_factory)
