from core.utils.repository import SQLAlchemyRepository
from db.models.sneakers import SneakerModel


class SneakerModelRepository(SQLAlchemyRepository[SneakerModel]):
    def __init__(self, session):
        super().__init__(SneakerModel, session)
