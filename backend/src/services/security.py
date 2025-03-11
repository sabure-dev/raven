from typing import Callable

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from core.exceptions import InvalidCredentialsException, TokenExpiredException
from db.models.users import User
from repositories.users import UserRepository
from services.jwt import TokenService


class SecurityService:
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

    def __init__(
            self,
            user_repo_factory: Callable[[], UserRepository],
            token_service_factory: Callable[[], TokenService]
    ):
        self.user_repo = user_repo_factory()
        self.token_service = token_service_factory()

    async def get_current_user(self, token: str) -> User:
        try:
            payload = self.token_service.verify_token(token)
            username = payload.get("sub")

            if not username:
                raise InvalidCredentialsException()

            user = await self.user_repo.find_one_by_field("username", username)

            if not user:
                raise InvalidCredentialsException()

            if not user.is_active:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Неактивный пользователь"
                )

            return user
        except (InvalidCredentialsException, TokenExpiredException) as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(e),
                headers={"WWW-Authenticate": "Bearer"}
            )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Невозможно проверить учетные данные",
                headers={"WWW-Authenticate": "Bearer"}
            )

    async def get_current_active_verified_user(self, current_user: User) -> User:
        if not current_user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Email не подтвержден"
            )
        return current_user

    async def get_current_superuser(self, current_user: User) -> User:
        if not current_user.is_superuser:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав"
            )
        return current_user
