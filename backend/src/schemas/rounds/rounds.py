from datetime import datetime
from enum import Enum as PyEnum

from pydantic import BaseModel

from schemas.bets.bets import BetOut
from schemas.sneaker_model.sneaker_model import SneakerModelOut


class RoundStatus(PyEnum):
    PLANNED = "planned"
    FINISHED = "finished"
    CANCELLED = "cancelled"


class RoundBase(BaseModel):
    pass


class RoundCreate(RoundBase):
    planned_time: datetime | None = None
    model_id: int


class RoundOut(RoundBase):
    id: int
    status: RoundStatus
    model: SneakerModelOut
    bets: list[BetOut] | None = None
    winner_id: int | None = None
    planned_time: datetime
    created_at: datetime
    closed_at: datetime | None = None
