from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, Query
from starlette import status

from core.dependencies.users.security import get_current_superuser
from core.dependencies.sneaker_model.use_cases import get_create_sneaker_model_use_case, get_get_sneaker_model_use_case, \
    get_get_sneakers_models_use_case, get_update_sneaker_model_use_case, get_delete_sneaker_model_use_case
from db.models.users import User
from schemas.sneaker_model.sneaker_model import SneakerModelCreate, SneakerModelOut, SneakerModelParams, \
    SneakerModelUpdate
from schemas.sneaker_model.use_cases import CreateSneakerModelInput, GetSneakerModelInput, GetSneakersModelsInput, \
    UpdateSneakerModelInput, DeleteSneakerModelInput

router = APIRouter(
    prefix="/sneaker_model",
    tags=["SneakerModel"],
)


@router.post("", response_model=dict[str, int], status_code=status.HTTP_201_CREATED)
async def create_sneaker_model(
        sneaker_model_to_create: Annotated[SneakerModelCreate, Body(title="Данные для создания модели кроссовок")],
        create_sneaker_model_use_case=Depends(get_create_sneaker_model_use_case),
        _: User = Depends(get_current_superuser),
):
    sneaker_model_id = await create_sneaker_model_use_case.execute(
        CreateSneakerModelInput(sneaker_model=sneaker_model_to_create)
    )
    return {"sneaker_model_id": sneaker_model_id}


@router.get("/{sneaker_model_id}", response_model=SneakerModelOut, status_code=status.HTTP_200_OK)
async def get_sneaker_model_by_id(
        sneaker_model_id: Annotated[int, Path(title="ID модели кроссовок")],
        get_sneaker_model_use_case=Depends(get_get_sneaker_model_use_case),
):
    sneaker_model = await get_sneaker_model_use_case.execute(
        GetSneakerModelInput(sneaker_model_id=sneaker_model_id)
    )
    return sneaker_model


@router.get("", response_model=list[SneakerModelOut], status_code=status.HTTP_200_OK)
async def get_sneakers_models_by_filters(
        sneaker_model_params: Annotated[SneakerModelParams, Query(title="Параметры для пользователя")],
        get_sneakers_models_use_case=Depends(get_get_sneakers_models_use_case),
):
    sneakers_models = await get_sneakers_models_use_case.execute(
        GetSneakersModelsInput(
            params=sneaker_model_params
        )
    )
    return sneakers_models


@router.patch("/{sneaker_model_id}", response_model=SneakerModelOut, status_code=status.HTTP_200_OK)
async def update_sneaker_model_by_id(
        sneaker_model_id: Annotated[int, Path(title="ID модели кроссовок")],
        update_sneaker_model: Annotated[SneakerModelUpdate, Body(title="Данные для изменения модели кроссовок")],
        update_sneaker_model_use_case=Depends(get_update_sneaker_model_use_case),
        _: User = Depends(get_current_superuser),
):
    updated_sneaker_model = await update_sneaker_model_use_case.execute(
        UpdateSneakerModelInput(
            sneaker_model_id=sneaker_model_id,
            update_sneaker_model=update_sneaker_model,
        )
    )
    return updated_sneaker_model


@router.delete("/{sneaker_model_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_sneaker_model_by_id(
        sneaker_model_id: Annotated[int, Path(title="ID модели кроссовок")],
        delete_sneaker_model_use_case=Depends(get_delete_sneaker_model_use_case),
        _: User = Depends(get_current_superuser),
):
    await delete_sneaker_model_use_case.execute(DeleteSneakerModelInput(sneaker_model_id=sneaker_model_id))
