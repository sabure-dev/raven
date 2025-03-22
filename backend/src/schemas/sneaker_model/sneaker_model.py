from pydantic import BaseModel


class SneakerModelBase(BaseModel):
    name: str
    brand: str
    type: str
    description: str
    price: float


class SneakerModelCreate(SneakerModelBase):
    pass


class SneakerModelOut(SneakerModelBase):
    id: int


class SneakerModelParams(BaseModel):
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
