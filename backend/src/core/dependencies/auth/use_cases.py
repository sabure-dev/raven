from typing import Callable

from fastapi import Depends

from core.dependencies.auth.services import get_auth_service_factory
from services.auth import AuthService
from use_cases.auth import AuthenticateUserUseCase, RefreshTokenUseCase


def get_authenticate_user_use_case(
        auth_service_factory: Callable[[], AuthService] = Depends(get_auth_service_factory),
) -> AuthenticateUserUseCase:
    return AuthenticateUserUseCase(auth_service_factory)


def get_refresh_token_use_case(
        auth_service_factory: Callable[[], AuthService] = Depends(get_auth_service_factory),
) -> RefreshTokenUseCase:
    return RefreshTokenUseCase(auth_service_factory)
