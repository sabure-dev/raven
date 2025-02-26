from datetime import datetime, timedelta, UTC

import jwt

from core.config.config import settings


def create_verification_token(email: str) -> str:
    expire = datetime.now(UTC) + timedelta(minutes=settings.api_settings.VERIFICATION_TOKEN_EXPIRE_MINUTES)
    data = {
        "exp": expire,
        "email": email
    }
    return jwt.encode(data, settings.api_settings.SECRET_KEY, algorithm="HS256")


def verify_token(token: str) -> str:
    try:
        payload = jwt.decode(token, settings.api_settings.SECRET_KEY, algorithms=["HS256"])
        email: str = payload.get("email")
        if email is None:
            raise ValueError("Invalid token")
        return email
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")
