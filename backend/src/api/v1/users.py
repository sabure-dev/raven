from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Body, status, Path, HTTPException, BackgroundTasks

from api.v1.dependencies import get_user_service
from schemas.users import UserOut, UserCreate
from services.users import UserService
from core.exceptions import UserNotFoundException, UserAlreadyExistsException, UserAlreadyVerifiedException

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("", response_model=list[UserOut], status_code=status.HTTP_200_OK)
async def get_users(
        user_service: Annotated[UserService, Depends(get_user_service)],
):
    users = await user_service.get_users()
    return users


@router.get("/{user_id}", response_model=Optional[UserOut], status_code=status.HTTP_200_OK)
async def get_user_by_id(
        user_service: Annotated[UserService, Depends(get_user_service)],
        user_id: Annotated[int, Path(title="ID of the user to get")],
):
    try:
        user = await user_service.get_user_by_id(user_id)
        return user
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("", response_model=dict[str, int], status_code=status.HTTP_201_CREATED)
async def create_user(
        background_tasks: BackgroundTasks,
        user_service: Annotated[UserService, Depends(get_user_service)],
        user_to_create: Annotated[UserCreate, Body(title="User to create")],
):
    try:
        user_id = await user_service.create_user(user_to_create, background_tasks)
        return {"user_id": user_id}
    except UserAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
        user_service: Annotated[UserService, Depends(get_user_service)],
        user_id: Annotated[int, Path(title="ID of the user to delete")],
):
    try:
        await user_service.delete_user(user_id)
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/verify/{token}", status_code=status.HTTP_200_OK)
async def verify_email(
        token: Annotated[str, Path()],
        user_service: Annotated[UserService, Depends(get_user_service)],
):
    try:
        await user_service.verify_email(token)
        return {"message": "Email successfully verified"}
    except (ValueError, UserNotFoundException, UserAlreadyVerifiedException) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
