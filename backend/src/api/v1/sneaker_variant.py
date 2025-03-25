from typing import Annotated

from fastapi import APIRouter, Body, Depends

from core.dependencies.sneaker_variant.use_cases import get_create_sneaker_variant_use_case
from core.dependencies.users.security import get_current_superuser
from db.models.users import User
from schemas.sneaker_variant.sneaker_variant import SneakerVariantOut, SneakerVariantCreate
from schemas.sneaker_variant.use_cases import CreateSneakerVariantInput

router = APIRouter(
    prefix="/sneaker_variant",
    tags=["SneakerVariant"]
)


@router.post("", response_model=SneakerVariantOut)
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
