from enum import Enum as PyEnum


class RoundStatus(PyEnum):
    PLANNED = "planned"
    ACCEPTING_BETS = "accepting_bets"
    FINISHED = "finished"
    CANCELLED = "cancelled"
