from core.utils.repository import SQLAlchemyRepository
from db.models.sneakers import SneakerVariant


class SneakerVariantRepository(SQLAlchemyRepository[SneakerVariant]):
    def __init__(self, session):
        super().__init__(SneakerVariant, session)
