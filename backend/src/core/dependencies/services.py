from typing import Callable

from fastapi import Depends

from core.dependencies.database import get_user_repository_factory
from repositories.users import UserRepository
from services.auth import AuthService
from services.email import EmailService
from services.jwt import TokenService
from services.security import SecurityService
from services.users import UserService


def get_token_service() -> TokenService:
    return TokenService()


def get_token_service_factory() -> Callable[[], TokenService]:
    return lambda: TokenService()


def get_email_service() -> EmailService:
    return EmailService()


def get_email_service_factory() -> Callable[[], EmailService]:
    return lambda: EmailService()


def get_user_service(
        user_repository_factory: Callable[[], UserRepository] = Depends(get_user_repository_factory)
) -> UserService:
    return UserService(user_repository_factory)


def get_user_service_factory(
        user_repository_factory: Callable[[], UserRepository] = Depends(get_user_repository_factory)
) -> Callable[[], UserService]:
    return lambda: UserService(user_repository_factory)


def get_auth_service(
        user_repository_factory: Callable[[], UserRepository] = Depends(get_user_repository_factory),
        token_service_factory: Callable[[], TokenService] = Depends(get_token_service_factory)
) -> AuthService:
    return AuthService(user_repository_factory, token_service_factory)


def get_auth_service_factory(
        user_repository_factory: Callable[[], UserRepository] = Depends(get_user_repository_factory),
        token_service_factory: Callable[[], TokenService] = Depends(get_token_service_factory)
) -> Callable[[], AuthService]:
    return lambda: AuthService(user_repository_factory, token_service_factory)


def get_security_service(
        user_repository_factory: Callable[[], UserRepository] = Depends(get_user_repository_factory),
        token_service_factory: Callable[[], TokenService] = Depends(get_token_service_factory)
) -> SecurityService:
    return SecurityService(user_repository_factory, token_service_factory)
