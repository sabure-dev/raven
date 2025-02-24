from core.utils.repository import SQLAlchemyRepository
from db.models.users import User


class UserRepository(SQLAlchemyRepository[User]):
    def __init__(self, session):
        super().__init__(User, session)
