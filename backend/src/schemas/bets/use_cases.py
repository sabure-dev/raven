from pydantic import BaseModel

from schemas.bets.bets import BetCreate, BetParams


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


class GetUserBetsInput(BaseModelWithConfig):
    params: BetParams
    user_id: int
