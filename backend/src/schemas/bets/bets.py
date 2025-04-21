from datetime import datetime
from typing import Optional, Literal

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


class BetParams(BaseModel):
    is_winner: bool | None = None
    is_actual: bool | None = None
    offset: int | None = None
    limit: int | None = None
    sort_by_date: Literal["asc", "desc"] | None = None


from schemas.rounds.rounds import RoundOut

BetOut.model_rebuild()
