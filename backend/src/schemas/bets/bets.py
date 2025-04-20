from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class BetBase(BaseModel):
    amount: float = Field(100, gt=0)


class BetCreate(BetBase):
    pass


class BetOut(BetBase):
    id: int
    round_id: int
    round: Optional["RoundOut"]
    user_id: int
    is_winner: bool
    created_at: datetime


from schemas.rounds.rounds import RoundOut

BetOut.model_rebuild()
