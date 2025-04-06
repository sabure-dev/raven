from typing import Literal

from pydantic import BaseModel, Field


class SneakerModelBase(BaseModel):
    name: str
    brand: str
    type: str
    description: str
    price: float = Field(..., ge=0)


class SneakerModelCreate(SneakerModelBase):
    pass


class SneakerModelOut(SneakerModelBase):
    id: int
    variants: list["SneakerVariantOut"] | None = None


class SneakerModelUpdate(BaseModel):
    name: str | None = None
    brand: str | None = None
    type: str | None = None
    description: str | None = None
    price: float | None = Field(None, ge=0)


class SneakerModelParams(BaseModel):
    sneaker_model_id: int | None = None
    name: str | None = None
    brand: str | None = None
    sneaker_model_type: str | None = None
    min_price: float | None = None
    max_price: float | None = None
    sizes: list[float] | None = None
    search_query: str | None = None
    include_variants: bool | None = None
    in_stock: bool | None = None
    offset: int | None = None
    limit: int | None = None
    sort_by_price: Literal["asc", "desc"] | None = None


from schemas.sneaker_variant.sneaker_variant import SneakerVariantOut

SneakerModelOut.model_rebuild()
