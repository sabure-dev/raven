from typing import List, Optional, Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Path, Body, BackgroundTasks
from pydantic import EmailStr

from api.v1.dependencies import (
    get_get_user_use_case, get_get_users_use_case, get_create_user_use_case,
    get_verify_email_use_case, get_delete_user_use_case, get_update_user_email_use_case,
    get_update_user_username_use_case, get_request_password_reset_use_case,
    get_update_password_use_case, get_user_service
)
from core.exceptions import (
    ItemNotFoundException, ItemAlreadyExistsException, UnverifiedEmailException,
    InvalidCredentialsException, UserAlreadyVerifiedException
)
from core.security.dependencies import (
    get_current_active_verified_user, get_current_superuser
)
from db.models.users import User
from schemas.users import UserOut, UserCreate, ChangePasswordRequest
from schemas.use_cases import (
    GetUserInput, DeleteUserInput, UpdateUserEmailInput,
    UpdateUserUsernameInput, VerifyEmailInput, RequestPasswordResetInput,
    UpdatePasswordInput, CreateUserInput
)
from services.users import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("", response_model=List[UserOut], status_code=status.HTTP_200_OK)
async def get_users(
        *,
        get_users_use_case=Depends(get_get_users_use_case),
        _: User = Depends(get_current_superuser)
):
    return await get_users_use_case.execute(None)


@router.get("/me", response_model=UserOut, status_code=status.HTTP_200_OK)
async def get_current_user_info(
        current_user: User = Depends(get_current_active_verified_user)
):
    return current_user.to_read_model()


@router.get("/{user_id}", response_model=Optional[UserOut], status_code=status.HTTP_200_OK)
async def get_user_by_id(
        user_id: Annotated[int, Path(title="ID пользователя")],
        get_user_use_case=Depends(get_get_user_use_case),
        _: User = Depends(get_current_superuser)
):
    try:
        user = await get_user_use_case.execute(GetUserInput(user_id=user_id))
        return user
    except ItemNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("", response_model=dict[str, int], status_code=status.HTTP_201_CREATED)
async def create_user(
        user_to_create: Annotated[UserCreate, Body(title="Данные для создания пользователя")],
        background_tasks: BackgroundTasks,
        create_user_use_case=Depends(get_create_user_use_case),
):
    try:
        user_id = await create_user_use_case.execute(
            CreateUserInput(user=user_to_create, background_tasks=background_tasks))
        return {"user_id": user_id}
    except ItemAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.post("/verify/{token}", status_code=status.HTTP_200_OK)
async def verify_email(
        token: Annotated[str, Path(title="Токен верификации")],
        verify_email_use_case=Depends(get_verify_email_use_case),
):
    try:
        await verify_email_use_case.execute(VerifyEmailInput(token=token))
        return {"message": "Email успешно подтвержден"}
    except (ItemNotFoundException, UserAlreadyVerifiedException, ValueError) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_current_user(
        delete_user_use_case=Depends(get_delete_user_use_case),
        current_user: User = Depends(get_current_active_verified_user)
):
    try:
        await delete_user_use_case.execute(DeleteUserInput(user_id=current_user.id))
    except ItemNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
        user_id: Annotated[int, Path(title="ID пользователя для удаления")],
        delete_user_use_case=Depends(get_delete_user_use_case),
        _: User = Depends(get_current_superuser)
):
    try:
        await delete_user_use_case.execute(DeleteUserInput(user_id=user_id))
    except ItemNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.patch("/me/email", response_model=UserOut, status_code=status.HTTP_200_OK)
async def update_current_user_email(
        new_email: Annotated[EmailStr, Body(title="Новый email")],
        background_tasks: BackgroundTasks,
        update_user_email_use_case=Depends(get_update_user_email_use_case),
        current_user: User = Depends(get_current_active_verified_user)
):
    try:
        updated_user = await update_user_email_use_case.execute(UpdateUserEmailInput(
            user_id=current_user.id,
            new_email=new_email,
            background_tasks=background_tasks
        ))
        return updated_user
    except ItemNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except ItemAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.patch("/{user_id}/email", response_model=UserOut, status_code=status.HTTP_200_OK)
async def update_user_email(
        user_id: Annotated[int, Path(title="ID пользователя для обновления")],
        new_email: Annotated[EmailStr, Body(title="Новый email")],
        background_tasks: BackgroundTasks,
        update_user_email_use_case=Depends(get_update_user_email_use_case),
        _: User = Depends(get_current_superuser)
):
    try:
        updated_user = await update_user_email_use_case.execute(UpdateUserEmailInput(
            user_id=user_id,
            new_email=new_email,
            background_tasks=background_tasks
        ))
        return updated_user
    except ItemNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except ItemAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.patch("/me/username", response_model=UserOut, status_code=status.HTTP_200_OK)
async def update_current_user_username(
        new_username: Annotated[str, Body(title="Новое имя пользователя")],
        update_user_username_use_case=Depends(get_update_user_username_use_case),
        current_user: User = Depends(get_current_active_verified_user)
):
    try:
        updated_user = await update_user_username_use_case.execute(UpdateUserUsernameInput(
            user_id=current_user.id,
            new_username=new_username
        ))
        return updated_user
    except ItemNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except (ItemAlreadyExistsException, UnverifiedEmailException) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.patch("/{user_id}/username", response_model=UserOut, status_code=status.HTTP_200_OK)
async def update_user_username(
        user_id: Annotated[int, Path(title="ID пользователя для обновления")],
        new_username: Annotated[str, Body(title="Новое имя пользователя")],
        update_user_username_use_case=Depends(get_update_user_username_use_case),
        _: User = Depends(get_current_superuser)
):
    try:
        updated_user = await update_user_username_use_case.execute(UpdateUserUsernameInput(
            user_id=user_id,
            new_username=new_username
        ))
        return updated_user
    except ItemNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except (ItemAlreadyExistsException, UnverifiedEmailException) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/password-reset", status_code=status.HTTP_200_OK)
async def request_password_reset(
        email: Annotated[EmailStr, Body(title="Email для сброса пароля")],
        background_tasks: BackgroundTasks,
        request_password_reset_use_case=Depends(get_request_password_reset_use_case),
):
    try:
        await request_password_reset_use_case.execute(RequestPasswordResetInput(
            email=email,
            background_tasks=background_tasks
        ))
        return {"message": "Инструкции по сбросу пароля отправлены на указанный email"}
    except (ItemNotFoundException, UnverifiedEmailException) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/password-reset/{token}", status_code=status.HTTP_200_OK)
async def update_password(
        token: Annotated[str, Path(title="Токен сброса пароля")],
        new_password: Annotated[str, Body(title="Новый пароль")],
        update_password_use_case=Depends(get_update_password_use_case),
):
    try:
        await update_password_use_case.execute(UpdatePasswordInput(token=token, new_password=new_password))
        return {"message": "Пароль успешно обновлен"}
    except (ItemNotFoundException, UnverifiedEmailException, ValueError) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.patch("/me/password", status_code=status.HTTP_200_OK)
async def change_current_user_password(
        password_data: Annotated[ChangePasswordRequest, Body(title="Данные для смены пароля")],
        current_user: User = Depends(get_current_active_verified_user),
        user_service: UserService = Depends(get_user_service)
):
    try:
        await user_service.change_password(
            current_user.id,
            password_data.current_password,
            password_data.new_password
        )
        return {"message": "Пароль успешно изменен"}
    except InvalidCredentialsException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
