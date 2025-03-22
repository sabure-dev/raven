from core.utils.repository import SQLAlchemyRepository
from db.models.sneakers import SneakerModel, SneakerVariant


class SneakerModelRepository(SQLAlchemyRepository[SneakerModel]):
    def __init__(self, session):
        super().__init__(SneakerModel, session)


class SneakerVariantRepository(SQLAlchemyRepository[SneakerVariant]):
    def __init__(self, session):
        super().__init__(SneakerVariant, session)
