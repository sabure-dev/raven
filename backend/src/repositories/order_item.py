from core.utils.repository import SQLAlchemyRepository
from db.models.orders import OrderItem


class OrderItemRepository(SQLAlchemyRepository[OrderItem]):
    def __init__(self, session):
        super().__init__(OrderItem, session)
