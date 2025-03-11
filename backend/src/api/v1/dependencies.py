from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.session.database import get_async_session
from repositories.users import UserRepository
from services.auth import AuthService
from services.email import EmailService
from services.jwt import TokenService
from services.security import SecurityService
from services.users import UserService
from use_cases.auth import AuthenticateUserUseCase, RefreshTokenUseCase
from use_cases.users import (
    CreateUserUseCase,
    VerifyEmailUseCase,
    GetUserUseCase,
    GetUsersUseCase,
    DeleteUserUseCase,
    UpdateUserEmailUseCase,
    UpdateUserUsernameUseCase,
    RequestPasswordResetUseCase,
    UpdatePasswordUseCase,
)


def get_user_repo_factory(session: AsyncSession = Depends(get_async_session)):
    return lambda: UserRepository(session)


def get_user_service_factory(user_repo_factory=Depends(get_user_repo_factory)):
    return lambda: UserService(user_repo_factory)


def get_token_service_factory():
    return lambda: TokenService()


def get_email_service_factory():
    return lambda: EmailService()


def get_security_service(
    user_repo_factory=Depends(get_user_repo_factory),
    token_service_factory=Depends(get_token_service_factory)
) -> SecurityService:
    return SecurityService(user_repo_factory, token_service_factory)


def get_auth_service_factory(
    user_repo_factory=Depends(get_user_repo_factory),
    token_service_factory=Depends(get_token_service_factory)
):
    return lambda: AuthService(user_repo_factory, token_service_factory)


def get_create_user_use_case(
    user_service_factory=Depends(get_user_service_factory),
    token_service_factory=Depends(get_token_service_factory),
    email_service_factory=Depends(get_email_service_factory)
) -> CreateUserUseCase:
    return CreateUserUseCase(user_service_factory, token_service_factory, email_service_factory)


def get_verify_email_use_case(
    user_service_factory=Depends(get_user_service_factory),
    token_service_factory=Depends(get_token_service_factory)
) -> VerifyEmailUseCase:
    return VerifyEmailUseCase(user_service_factory, token_service_factory)


def get_get_user_use_case(
    user_service_factory=Depends(get_user_service_factory)
) -> GetUserUseCase:
    return GetUserUseCase(user_service_factory)


def get_get_users_use_case(
    user_service_factory=Depends(get_user_service_factory),
) -> GetUsersUseCase:
    return GetUsersUseCase(user_service_factory)


def get_delete_user_use_case(
    user_service_factory=Depends(get_user_service_factory)
) -> DeleteUserUseCase:
    return DeleteUserUseCase(user_service_factory)


def get_update_user_email_use_case(
    user_service_factory=Depends(get_user_service_factory),
    token_service_factory=Depends(get_token_service_factory),
    email_service_factory=Depends(get_email_service_factory)
) -> UpdateUserEmailUseCase:
    return UpdateUserEmailUseCase(user_service_factory, token_service_factory, email_service_factory)


def get_update_user_username_use_case(
    user_service_factory=Depends(get_user_service_factory)
) -> UpdateUserUsernameUseCase:
    return UpdateUserUsernameUseCase(user_service_factory)


def get_request_password_reset_use_case(
    user_service_factory=Depends(get_user_service_factory),
    token_service_factory=Depends(get_token_service_factory),
    email_service_factory=Depends(get_email_service_factory)
) -> RequestPasswordResetUseCase:
    return RequestPasswordResetUseCase(user_service_factory, token_service_factory, email_service_factory)


def get_update_password_use_case(
    user_service_factory=Depends(get_user_service_factory),
    token_service_factory=Depends(get_token_service_factory)
) -> UpdatePasswordUseCase:
    return UpdatePasswordUseCase(user_service_factory, token_service_factory)


def get_authenticate_user_use_case(
    auth_service_factory=Depends(get_auth_service_factory)
) -> AuthenticateUserUseCase:
    return AuthenticateUserUseCase(auth_service_factory)


def get_refresh_token_use_case(
    auth_service_factory=Depends(get_auth_service_factory)
) -> RefreshTokenUseCase:
    return RefreshTokenUseCase(auth_service_factory)


def get_user_service(session: AsyncSession = Depends(get_async_session)) -> UserService:
    return UserService(lambda: UserRepository(session))
