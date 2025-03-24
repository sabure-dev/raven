from typing import Annotated

from fastapi import APIRouter, Depends, status, Path, Body
from pydantic import EmailStr

from core.dependencies.users.use_cases import (
    get_create_user_use_case,
    get_verify_email_use_case,
    get_get_user_use_case,
    get_delete_user_use_case,
    get_update_user_email_use_case,
    get_update_user_username_use_case,
    get_request_password_reset_use_case,
    get_update_password_use_case,
    get_change_password_use_case,
)
from core.dependencies.users.security import (
    get_current_active_verified_user,
    get_current_superuser,
)
from db.models.users import User
from schemas.users.users import UserOut, UserCreate, ChangePasswordRequest
from schemas.users.use_cases import (
    GetUserInput,
    DeleteUserInput,
    UpdateUserEmailInput,
    UpdateUserUsernameInput,
    VerifyEmailInput,
    RequestPasswordResetInput,
    UpdatePasswordInput,
    CreateUserInput,
    ChangePasswordInput,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/me", response_model=UserOut, status_code=status.HTTP_200_OK)
async def get_current_user_info(
        current_user: User = Depends(get_current_active_verified_user),
):
    return current_user.to_read_model()


@router.get("/{user_id}", response_model=UserOut, status_code=status.HTTP_200_OK)
async def get_user_by_id(
        user_id: Annotated[int, Path(title="ID пользователя")],
        get_user_use_case=Depends(get_get_user_use_case),
        _: User = Depends(get_current_superuser),
):
    user = await get_user_use_case.execute(GetUserInput(user_id=user_id))
    return user


@router.post("", response_model=dict[str, int], status_code=status.HTTP_201_CREATED)
async def create_user(
        user_to_create: Annotated[
            UserCreate, Body(title="Данные для создания пользователя")
        ],
        create_user_use_case=Depends(get_create_user_use_case),
):
    user_id = await create_user_use_case.execute(CreateUserInput(user=user_to_create))
    return {"user_id": user_id}


@router.post("/verify/{token}", status_code=status.HTTP_200_OK)
async def verify_email(
        token: Annotated[str, Path(title="Токен верификации")],
        verify_email_use_case=Depends(get_verify_email_use_case),
):
    await verify_email_use_case.execute(VerifyEmailInput(token=token))
    return {"message": "Email успешно подтвержден"}


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_current_user(
        delete_user_use_case=Depends(get_delete_user_use_case),
        current_user: User = Depends(get_current_active_verified_user),
):
    await delete_user_use_case.execute(DeleteUserInput(user_id=current_user.id))


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
        user_id: Annotated[int, Path(title="ID пользователя для удаления")],
        delete_user_use_case=Depends(get_delete_user_use_case),
        _: User = Depends(get_current_superuser),
):
    await delete_user_use_case.execute(DeleteUserInput(user_id=user_id))


@router.patch("/me/email", response_model=UserOut, status_code=status.HTTP_200_OK)
async def update_current_user_email(
        new_email: Annotated[EmailStr, Body(title="Новый email")],
        update_user_email_use_case=Depends(get_update_user_email_use_case),
        current_user: User = Depends(get_current_active_verified_user),
):
    updated_user = await update_user_email_use_case.execute(
        UpdateUserEmailInput(
            user_id=current_user.id,
            new_email=new_email,
        )
    )
    return updated_user


@router.patch(
    "/{user_id}/email", response_model=UserOut, status_code=status.HTTP_200_OK
)
async def update_user_email(
        user_id: Annotated[int, Path(title="ID пользователя для обновления")],
        new_email: Annotated[EmailStr, Body(title="Новый email")],
        update_user_email_use_case=Depends(get_update_user_email_use_case),
        _: User = Depends(get_current_superuser),
):
    updated_user = await update_user_email_use_case.execute(
        UpdateUserEmailInput(
            user_id=user_id,
            new_email=new_email,
        )
    )
    return updated_user


@router.patch("/me/username", response_model=UserOut, status_code=status.HTTP_200_OK)
async def update_current_user_username(
        new_username: Annotated[str, Body(title="Новое имя пользователя", min_length=3)],
        update_user_username_use_case=Depends(get_update_user_username_use_case),
        current_user: User = Depends(get_current_active_verified_user),
):
    updated_user = await update_user_username_use_case.execute(
        UpdateUserUsernameInput(user_id=current_user.id, new_username=new_username)
    )
    return updated_user


@router.patch(
    "/{user_id}/username", response_model=UserOut, status_code=status.HTTP_200_OK
)
async def update_user_username(
        user_id: Annotated[int, Path(title="ID пользователя для обновления")],
        new_username: Annotated[str, Body(title="Новое имя пользователя", min_length=3)],
        update_user_username_use_case=Depends(get_update_user_username_use_case),
        _: User = Depends(get_current_superuser),
):
    updated_user = await update_user_username_use_case.execute(
        UpdateUserUsernameInput(user_id=user_id, new_username=new_username)
    )
    return updated_user


@router.post("/password-reset", status_code=status.HTTP_200_OK)
async def request_password_reset(
        email: Annotated[EmailStr, Body(title="Email для сброса пароля")],
        request_password_reset_use_case=Depends(get_request_password_reset_use_case),
):
    await request_password_reset_use_case.execute(
        RequestPasswordResetInput(
            email=email,
        )
    )
    return {"message": "Инструкции по сбросу пароля отправлены на указанный email"}


@router.post("/password-reset/{token}", status_code=status.HTTP_200_OK)
async def update_password(
        token: Annotated[str, Path(title="Токен сброса пароля")],
        new_password: Annotated[str, Body(title="Новый пароль", min_length=8)],
        update_password_use_case=Depends(get_update_password_use_case),
):
    await update_password_use_case.execute(
        UpdatePasswordInput(token=token, new_password=new_password)
    )
    return {"message": "Пароль успешно обновлен"}


@router.patch("/me/password", status_code=status.HTTP_200_OK)
async def change_current_user_password(
        password_data: Annotated[
            ChangePasswordRequest, Body(title="Данные для смены пароля")
        ],
        current_user: User = Depends(get_current_active_verified_user),
        change_password_use_case=Depends(get_change_password_use_case),
):
    await change_password_use_case.execute(
        ChangePasswordInput(
            user_id=current_user.id,
            current_password=password_data.current_password,
            new_password=password_data.new_password,
        )
    )
    return {"message": "Пароль успешно изменен"}
