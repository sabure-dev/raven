from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from api.v1.dependencies import get_authenticate_user_use_case, get_refresh_token_use_case
from core.exceptions import AuthException
from schemas.auth import TokenResponse, LoginRequest, RefreshTokenRequest
from use_cases.auth import AuthenticateUserUseCase, RefreshTokenUseCase

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse)
async def login(
        credentials: LoginRequest,
        authenticate_user_use_case: Annotated[AuthenticateUserUseCase, Depends(get_authenticate_user_use_case)]
):
    try:
        return await authenticate_user_use_case.execute(credentials)
    except AuthException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
        request: RefreshTokenRequest,
        refresh_token_use_case: Annotated[RefreshTokenUseCase, Depends(get_refresh_token_use_case)]
):
    try:
        return await refresh_token_use_case.execute(request)
    except AuthException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
