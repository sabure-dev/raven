from datetime import timedelta, datetime, UTC

from core.config.config import settings
from core.exceptions import InvalidCredentialsException, TokenExpiredException
from db.models.users import User
from schemas.auth import TokenResponse

import jwt


class TokenService:
    def __init__(self):
        with open(settings.auth_jwt.private_key_path, 'r') as f:
            self.private_key = f.read()
        with open(settings.auth_jwt.public_key_path, 'r') as f:
            self.public_key = f.read()

    def create_tokens(self, user: User) -> TokenResponse:
        access_token = self._create_token(
            "username",
            user,
            timedelta(minutes=settings.auth_jwt.access_token_expire_minutes)
        )
        refresh_token = self._create_token(
            "username",
            user,
            timedelta(days=settings.auth_jwt.refresh_token_expire_days)
        )
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token
        )

    def create_verification_token(self, user: User) -> str:
        verification_token = self._create_token(
            "username",
            user,
            timedelta(minutes=settings.auth_jwt.verification_token_expire_minutes)
        )
        return verification_token

    def verify_token(self, token: str) -> dict:
        try:
            return jwt.decode(
                token,
                self.public_key,
                algorithms=[settings.auth_jwt.algorithm],
            )
        except jwt.ExpiredSignatureError:
            raise TokenExpiredException()
        except jwt.InvalidTokenError:
            raise InvalidCredentialsException()

    def _create_token(self, sub_type: str, user: User, expires_delta: timedelta) -> str:
        expire = datetime.now(UTC) + expires_delta
        to_encode = {
            "exp": expire,
            "sub": getattr(user, sub_type),
        }
        return jwt.encode(
            to_encode,
            self.private_key,
            algorithm=settings.auth_jwt.algorithm
        )
