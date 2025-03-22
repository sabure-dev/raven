from typing import Callable

from fastapi import Depends, BackgroundTasks

from core.dependencies.users.services import (
    get_user_service_factory, get_token_service_factory,
)
from core.dependencies.email.services import get_email_service_factory
from services.email import EmailService
from services.jwt import TokenService
from services.users import UserService
from use_cases.users import (
    CreateUserUseCase, VerifyEmailUseCase, GetUserUseCase, GetUsersUseCase,
    DeleteUserUseCase, UpdateUserEmailUseCase, UpdateUserUsernameUseCase,
    RequestPasswordResetUseCase, UpdatePasswordUseCase, ChangePasswordUseCase
)


def get_create_user_use_case(
        background_tasks: BackgroundTasks,
        user_service_factory: Callable[[], UserService] = Depends(get_user_service_factory),
        token_service_factory: Callable[[], TokenService] = Depends(get_token_service_factory),
        email_service_factory: Callable[[], EmailService] = Depends(get_email_service_factory),
) -> CreateUserUseCase:
    return CreateUserUseCase(user_service_factory, token_service_factory, email_service_factory, background_tasks)


def get_verify_email_use_case(
        user_service_factory: Callable[[], UserService] = Depends(get_user_service_factory),
        token_service_factory: Callable[[], TokenService] = Depends(get_token_service_factory)
) -> VerifyEmailUseCase:
    return VerifyEmailUseCase(user_service_factory, token_service_factory)


def get_get_user_use_case(
        user_service_factory: Callable[[], UserService] = Depends(get_user_service_factory)
) -> GetUserUseCase:
    return GetUserUseCase(user_service_factory)


def get_get_users_use_case(
        user_service_factory: Callable[[], UserService] = Depends(get_user_service_factory)
) -> GetUsersUseCase:
    return GetUsersUseCase(user_service_factory)


def get_delete_user_use_case(
        user_service_factory: Callable[[], UserService] = Depends(get_user_service_factory)
) -> DeleteUserUseCase:
    return DeleteUserUseCase(user_service_factory)


def get_update_user_email_use_case(
        background_tasks: BackgroundTasks,
        user_service_factory: Callable[[], UserService] = Depends(get_user_service_factory),
        token_service_factory: Callable[[], TokenService] = Depends(get_token_service_factory),
        email_service_factory: Callable[[], EmailService] = Depends(get_email_service_factory)
) -> UpdateUserEmailUseCase:
    return UpdateUserEmailUseCase(user_service_factory, token_service_factory, email_service_factory, background_tasks)


def get_update_user_username_use_case(
        user_service_factory: Callable[[], UserService] = Depends(get_user_service_factory)
) -> UpdateUserUsernameUseCase:
    return UpdateUserUsernameUseCase(user_service_factory)


def get_request_password_reset_use_case(
        background_tasks: BackgroundTasks,
        user_service_factory: Callable[[], UserService] = Depends(get_user_service_factory),
        token_service_factory: Callable[[], TokenService] = Depends(get_token_service_factory),
        email_service_factory: Callable[[], EmailService] = Depends(get_email_service_factory)
) -> RequestPasswordResetUseCase:
    return RequestPasswordResetUseCase(user_service_factory, token_service_factory, email_service_factory,
                                       background_tasks)


def get_update_password_use_case(
        user_service_factory: Callable[[], UserService] = Depends(get_user_service_factory),
        token_service_factory: Callable[[], TokenService] = Depends(get_token_service_factory)
) -> UpdatePasswordUseCase:
    return UpdatePasswordUseCase(user_service_factory, token_service_factory)


def get_change_password_use_case(
        user_service_factory: Callable[[], UserService] = Depends(get_user_service_factory)
) -> ChangePasswordUseCase:
    return ChangePasswordUseCase(user_service_factory)
