from core.utils.repository import SQLAlchemyRepository
from db.models.orders import Order


class OrderRepository(SQLAlchemyRepository[Order]):
    def __init__(self, session):
        super().__init__(Order, session)
