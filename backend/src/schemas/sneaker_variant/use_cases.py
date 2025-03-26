from pydantic import BaseModel

from schemas.sneaker_variant.sneaker_variant import SneakerVariantCreate


class BaseModelWithConfig(BaseModel):
    model_config = {
        "arbitrary_types_allowed": True,
    }


class CreateSneakerVariantInput(BaseModelWithConfig):
    sneaker_variant: SneakerVariantCreate


class UpdateSneakerVariantQuantityInput(BaseModelWithConfig):
    sneaker_variant_id: int
    quantity_delta: int


class DeleteSneakerVariantInput(BaseModelWithConfig):
    sneaker_variant_id: int
