from datetime import datetime

from pydantic import BaseModel


class BetBase(BaseModel):
    amount: float


class BetCreate(BetBase):
    pass


class BetOut(BetBase):
    round_id: int
    id: int
    user_id: int
    is_winner: bool
    created_at: datetime
