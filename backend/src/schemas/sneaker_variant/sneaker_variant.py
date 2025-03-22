from pydantic import BaseModel


class SneakerVariantBase(BaseModel):
    model_id: int
    size: float
    quantity: int


class SneakerVariantCreate(SneakerVariantBase):
    pass


class SneakerVariantOut(SneakerVariantBase):
    id: int
