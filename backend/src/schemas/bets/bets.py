from datetime import datetime

from pydantic import BaseModel


class BetBase(BaseModel):
    round_id: int
    amount: float


class BetCreate(BetBase):
    pass


class BetOut(BetBase):
    id: int
    user_id: int
    is_winner: bool
    created_at: datetime
