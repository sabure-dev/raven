from pydantic import BaseModel

from schemas.sneaker_model.sneaker_model import SneakerModelCreate, SneakerModelParams, SneakerModelUpdate


class BaseModelWithConfig(BaseModel):
    model_config = {
        "arbitrary_types_allowed": True,
    }


class CreateSneakerModelInput(BaseModelWithConfig):
    sneaker_model: SneakerModelCreate


class GetSneakersModelsInput(BaseModelWithConfig):
    params: SneakerModelParams


class GetSneakerModelInput(BaseModelWithConfig):
    sneaker_model_id: int


class UpdateSneakerModelInput(BaseModelWithConfig):
    sneaker_model_id: int
    update_sneaker_model: SneakerModelUpdate


class DeleteSneakerModelInput(BaseModelWithConfig):
    sneaker_model_id: int
