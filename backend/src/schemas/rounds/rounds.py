from datetime import datetime, timedelta, timezone
from enum import Enum as PyEnum

from pydantic import BaseModel, Field

from schemas.sneaker_model.sneaker_model import SneakerModelOut


class RoundStatus(PyEnum):
    PLANNED = "planned"
    FINISHED = "finished"
    CANCELLED = "cancelled"


class RoundBase(BaseModel):
    min_bet_amount: int = Field(100, gt=0)


class RoundCreate(RoundBase):
    planned_time: datetime | None = datetime.now(timezone.utc) + timedelta(days=1)
    model_id: int


class RoundOut(RoundBase):
    id: int
    status: RoundStatus
    model: SneakerModelOut | None = None
    bets: list["BetOut"] | None = None
    winner_id: int | None = None
    planned_time: datetime
    created_at: datetime
    closed_at: datetime | None = None


from schemas.bets.bets import BetOut

RoundOut.model_rebuild()
