from core.utils.repository import SQLAlchemyRepository
from db.models.rounds import Round


class RoundRepository(SQLAlchemyRepository[Round]):
    def __init__(self, session):
        super().__init__(Round, session)
