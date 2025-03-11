from fastapi import Depends

from api.v1.dependencies import get_security_service
from db.models.users import User
from services.security import SecurityService


async def get_current_user(
        token: str = Depends(SecurityService.oauth2_scheme),
        security_service: SecurityService = Depends(get_security_service)
) -> User:
    return await security_service.get_current_user(token)


async def get_current_active_verified_user(
        current_user: User = Depends(get_current_user),
        security_service: SecurityService = Depends(get_security_service)
) -> User:
    return await security_service.get_current_active_verified_user(current_user)


async def get_current_superuser(
        current_user: User = Depends(get_current_user),
        security_service: SecurityService = Depends(get_security_service)
) -> User:
    return await security_service.get_current_superuser(current_user)
