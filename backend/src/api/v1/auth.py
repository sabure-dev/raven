from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from api.v1.dependencies import get_auth_service
from core.exceptions import AuthException
from schemas.auth import TokenResponse, LoginRequest, RefreshTokenRequest
from services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse)
async def login(
        credentials: LoginRequest,
        auth_service: Annotated[AuthService, Depends(get_auth_service)]
):
    try:
        return await auth_service.authenticate_user(credentials)
    except AuthException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
        request: RefreshTokenRequest,
        auth_service: Annotated[AuthService, Depends(get_auth_service)]
):
    try:
        return await auth_service.refresh_token(request.refresh_token)
    except AuthException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
