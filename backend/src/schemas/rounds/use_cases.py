from pydantic import BaseModel

from schemas.rounds.rounds import (
    RoundCreate,
)


class BaseModelWithConfig(BaseModel):
    model_config = {
        "arbitrary_types_allowed": True,
    }


class CreateRoundInput(BaseModelWithConfig):
    round: RoundCreate
