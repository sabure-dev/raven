from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from core.dependencies import get_authenticate_user_use_case, get_refresh_token_use_case
from schemas.auth import TokenResponse, RefreshTokenRequest
from use_cases.auth import AuthenticateUserUseCase, RefreshTokenUseCase

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse)
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        authenticate_user_use_case: Annotated[AuthenticateUserUseCase, Depends(get_authenticate_user_use_case)]
):
    tokens = await authenticate_user_use_case.execute(form_data)
    return tokens


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
        request: RefreshTokenRequest,
        refresh_token_use_case: Annotated[RefreshTokenUseCase, Depends(get_refresh_token_use_case)]
):
    return await refresh_token_use_case.execute(request)
