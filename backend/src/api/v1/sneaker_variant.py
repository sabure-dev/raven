from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, Query
from starlette import status

from core.dependencies.sneaker_variant.use_cases import get_create_sneaker_variant_use_case, \
    get_update_sneaker_variant_quantity_use_case, get_delete_sneaker_variant_use_case, get_get_sneaker_variant_use_case
from core.dependencies.users.security import get_current_superuser
from db.models.users import User
from schemas.sneaker_variant.sneaker_variant import SneakerVariantOut, SneakerVariantCreate
from schemas.sneaker_variant.use_cases import CreateSneakerVariantInput, UpdateSneakerVariantQuantityInput, \
    DeleteSneakerVariantInput, GetSneakerVariantInput

router = APIRouter(
    prefix="/sneaker_variant",
    tags=["SneakerVariant"]
)


@router.get("/{sneaker_variant_id}", response_model=SneakerVariantOut, status_code=status.HTTP_200_OK)
async def get_sneaker_variant(
        sneaker_variant_id: Annotated[int, Path(title="ID of sneaker variant")],
        get_sneaker_variant_use_case=Depends(get_get_sneaker_variant_use_case),
):
    sneaker_variant = await get_sneaker_variant_use_case.execute(
        GetSneakerVariantInput(sneaker_variant_id=sneaker_variant_id)
    )
    return sneaker_variant


@router.post("", response_model=SneakerVariantOut, status_code=status.HTTP_201_CREATED)
async def create_sneaker_variant(
        sneaker_variant_to_create: Annotated[
            SneakerVariantCreate, Body(title="Data for creating sneaker variant")
        ],
        create_sneaker_variant_use_case=Depends(get_create_sneaker_variant_use_case),
        _: User = Depends(get_current_superuser),
):
    sneaker_variant = await create_sneaker_variant_use_case.execute(
        CreateSneakerVariantInput(sneaker_variant=sneaker_variant_to_create)
    )
    return sneaker_variant


@router.patch("/{sneaker_variant_id}", response_model=SneakerVariantOut, status_code=status.HTTP_200_OK)
async def update_sneaker_variant_quantity(
        sneaker_variant_id: Annotated[int, Path(title="ID of sneaker variant")],
        quantity_delta: Annotated[int, Query(title="Quantity delta")],
        update_sneaker_variant_use_case=Depends(get_update_sneaker_variant_quantity_use_case),
        _: User = Depends(get_current_superuser),
):
    sneaker_variant = await update_sneaker_variant_use_case.execute(
        UpdateSneakerVariantQuantityInput(sneaker_variant_id=sneaker_variant_id, quantity_delta=quantity_delta)
    )
    return sneaker_variant


@router.delete("/{sneaker_variant_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_sneaker_variant(
        sneaker_variant_id: Annotated[int, Path(title="ID of sneaker variant")],
        delete_sneaker_variant_use_case=Depends(get_delete_sneaker_variant_use_case),
        _: User = Depends(get_current_superuser),
):
    await delete_sneaker_variant_use_case.execute(
        DeleteSneakerVariantInput(sneaker_variant_id=sneaker_variant_id)
    )
