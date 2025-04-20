from pydantic import BaseModel

from schemas.bets.bets import BetCreate


class BaseModelWithConfig(BaseModel):
    model_config = {
        "arbitrary_types_allowed": True,
    }


class CreateBetInput(BaseModelWithConfig):
    bet: BetCreate
    user_id: int


class IncreaseBetAmountInput(BaseModelWithConfig):
    delta: float
    user_id: int
