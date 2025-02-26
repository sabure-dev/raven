from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.session.database import get_async_session
from repositories.users import UserRepository
from services.auth import AuthService
from services.users import UserService


def get_user_service(session: AsyncSession = Depends(get_async_session)) -> UserService:
    return UserService(lambda: UserRepository(session))


def get_auth_service(session: AsyncSession = Depends(get_async_session)) -> AuthService:
    return AuthService(lambda: UserRepository(session))
