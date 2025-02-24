from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Body, status, Path

from api.v1.dependencies import get_user_service
from schemas.users import UserOut, UserCreate
from services.users import UserService

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
    user = await user_service.get_user_by_id(user_id)
    return user


@router.post("", response_model=dict[str, int], status_code=status.HTTP_201_CREATED)
async def create_user(
        user_service: Annotated[UserService, Depends(get_user_service)],
        user_to_create: Annotated[UserCreate, Body(title="User to create")],
):
    user_id = await user_service.create_user(user_to_create)
    return {"user_id": user_id}


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
        user_service: Annotated[UserService, Depends(get_user_service)],
        user_id: Annotated[int, Path(title="ID of the user to delete")],
):
    await user_service.delete_user(user_id)
    return
