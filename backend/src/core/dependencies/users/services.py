from typing import Callable

from fastapi import Depends

from core.dependencies.jwt.services import get_token_service_factory
from core.dependencies.users.database import get_user_repository_factory
from repositories.users import UserRepository
from services.jwt import TokenService
from services.security import SecurityService
from services.users import UserService


def get_user_service_factory(
        user_repository_factory: Callable[[], UserRepository] = Depends(
            get_user_repository_factory
        ),
) -> Callable[[], UserService]:
    return lambda: UserService(user_repository_factory)


def get_security_service_factory(
        user_service_factory: Callable[[], UserService] = Depends(get_user_service_factory),
        token_service_factory: Callable[[], TokenService] = Depends(
            get_token_service_factory
        ),
) -> Callable[[], SecurityService]:
    return lambda: SecurityService(user_service_factory, token_service_factory)
