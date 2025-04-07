from pydantic import BaseModel, Field


class SneakerVariantBase(BaseModel):
    model_id: int
    size: float = Field(..., gt=0)
    quantity: int = Field(..., ge=0)


class SneakerVariantCreate(SneakerVariantBase):
    pass


class SneakerVariantOut(SneakerVariantBase):
    id: int


class SneakerVariantOutWithModel(SneakerVariantOut):
    sneaker_model: "SneakerModelOut"


from schemas.sneaker_model.sneaker_model import SneakerModelOut

SneakerVariantOutWithModel.model_rebuild()
