from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Body, status, Path, HTTPException, BackgroundTasks
from pydantic import EmailStr

from api.v1.dependencies import (
    get_create_user_use_case,
    get_verify_email_use_case,
    get_get_user_use_case,
    get_get_users_use_case,
    get_delete_user_use_case,
    get_update_user_email_use_case,
    get_update_user_username_use_case,
    get_request_password_reset_use_case,
    get_update_password_use_case,
)
from core.exceptions import (
    UserNotFoundException,
    UserAlreadyExistsException,
    UserAlreadyVerifiedException,
    UnverifiedEmailException,
)
from schemas.users import UserOut, UserCreate
from schemas.use_cases import (
    CreateUserInput,
    DeleteUserInput,
    GetUserInput,
    RequestPasswordResetInput,
    UpdatePasswordInput,
    UpdateUserEmailInput,
    UpdateUserUsernameInput,
    VerifyEmailInput,
)


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("", response_model=list[UserOut], status_code=status.HTTP_200_OK)
async def get_users(
        *,
        get_users_use_case=Depends(get_get_users_use_case),
):
    users = await get_users_use_case.execute(None)
    return users


@router.get("/{user_id}", response_model=Optional[UserOut], status_code=status.HTTP_200_OK)
async def get_user_by_id(
        user_id: Annotated[int, Path(title="ID of the user to get")],
        get_user_use_case=Depends(get_get_user_use_case),
):
    try:
        user = await get_user_use_case.execute(GetUserInput(user_id=user_id))
        return user
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("", response_model=dict[str, int], status_code=status.HTTP_201_CREATED)
async def create_user(
        user_to_create: Annotated[UserCreate, Body(title="User to create")],
        background_tasks: BackgroundTasks,
        create_user_use_case=Depends(get_create_user_use_case),
):
    try:
        user_id = await create_user_use_case.execute(CreateUserInput(user=user_to_create, background_tasks=background_tasks))
        return {"user_id": user_id}
    except UserAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.post("/verify/{token}", status_code=status.HTTP_200_OK)
async def verify_email(
        token: Annotated[str, Path(title="Verification token")],
        verify_email_use_case=Depends(get_verify_email_use_case),
):
    try:
        await verify_email_use_case.execute(VerifyEmailInput(token=token))
    except (UserNotFoundException, UserAlreadyVerifiedException, ValueError) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
        user_id: Annotated[int, Path(title="ID of the user to delete")],
        delete_user_use_case=Depends(get_delete_user_use_case),
):
    try:
        await delete_user_use_case.execute(DeleteUserInput(user_id=user_id))
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.patch("/{user_id}/email", response_model=UserOut, status_code=status.HTTP_200_OK)
async def update_user_email(
        user_id: Annotated[int, Path(title="ID of the user to update")],
        new_email: Annotated[EmailStr, Body(title="New email")],
        background_tasks: BackgroundTasks,
        update_user_email_use_case=Depends(get_update_user_email_use_case),
):
    try:
        updated_user = await update_user_email_use_case.execute(UpdateUserEmailInput(
            user_id=user_id,
            new_email=new_email,
            background_tasks=background_tasks
        ))
        return updated_user
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except UserAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.patch("/{user_id}/username", response_model=UserOut, status_code=status.HTTP_200_OK)
async def update_user_username(
        user_id: Annotated[int, Path(title="ID of the user to update")],
        new_username: Annotated[str, Body(title="New username")],
        update_user_username_use_case=Depends(get_update_user_username_use_case),
):
    try:
        updated_user = await update_user_username_use_case.execute(UpdateUserUsernameInput(
            user_id=user_id,
            new_username=new_username
        ))
        return updated_user
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except (UserAlreadyExistsException, UnverifiedEmailException) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/password-reset", status_code=status.HTTP_200_OK)
async def request_password_reset(
        email: Annotated[EmailStr, Body(title="Email to reset password for")],
        background_tasks: BackgroundTasks,
        request_password_reset_use_case=Depends(get_request_password_reset_use_case),
):
    try:
        await request_password_reset_use_case.execute(RequestPasswordResetInput(email=email, background_tasks=background_tasks))
    except (UserNotFoundException, UnverifiedEmailException) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/password-reset/{token}", status_code=status.HTTP_200_OK)
async def update_password(
        token: Annotated[str, Path(title="Password reset token")],
        new_password: Annotated[str, Body(title="New password")],
        update_password_use_case=Depends(get_update_password_use_case),
):
    try:
        await update_password_use_case.execute(UpdatePasswordInput(token=token, new_password=new_password))
    except (UserNotFoundException, UnverifiedEmailException, ValueError) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
