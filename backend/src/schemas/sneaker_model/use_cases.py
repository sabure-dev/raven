from pydantic import BaseModel

from schemas.sneaker_model.sneaker_model import SneakerModelCreate, SneakerModelParams


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
