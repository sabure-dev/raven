from typing import Optional, Callable

from core.utils.repository import AbstractRepository
from schemas.users import UserOut, UserCreate


class UserService:
    def __init__(self, user_repo_factory: Callable[[], AbstractRepository]):
        self.user_repo = user_repo_factory()

    async def create_user(self, user: UserCreate) -> int:
        user_dict = user.model_dump()
        user_id = await self.user_repo.create_one(user_dict)
        return user_id

    async def get_user_by_id(self, user_id: int) -> Optional[UserOut]:
        user = await self.user_repo.find_one_by_id(user_id)
        if user:
            return user.to_read_model()
        return None

    async def get_users(self) -> list[UserOut]:
        users = await self.user_repo.find_all()
        if users:
            users = [user.to_read_model() for user in users]
        return users

    async def delete_user(self, user_id: int) -> None:
        await self.user_repo.delete_one(user_id)
