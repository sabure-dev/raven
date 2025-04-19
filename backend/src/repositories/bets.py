from core.utils.repository import SQLAlchemyRepository
from db.models.bets import Bet


class BetRepository(SQLAlchemyRepository[Bet]):
    def __init__(self, session):
        super().__init__(Bet, session)
