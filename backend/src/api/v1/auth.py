from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from api.v1.dependencies import get_authenticate_user_use_case, get_refresh_token_use_case
from core.exceptions import AuthException
from schemas.auth import TokenResponse, RefreshTokenRequest
from use_cases.auth import AuthenticateUserUseCase, RefreshTokenUseCase

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse)
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        authenticate_user_use_case: Annotated[AuthenticateUserUseCase, Depends(get_authenticate_user_use_case)]
):
    try:
        tokens = await authenticate_user_use_case.execute(form_data)
        return tokens
    except AuthException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Внутренняя ошибка сервера: {e}"
        )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
        request: RefreshTokenRequest,
        refresh_token_use_case: Annotated[RefreshTokenUseCase, Depends(get_refresh_token_use_case)]
):
    try:
        return await refresh_token_use_case.execute(request)
    except AuthException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Внутренняя ошибка сервера: {e}"
        )
