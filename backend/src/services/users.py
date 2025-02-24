from typing import Callable

from core.exceptions import UserAlreadyExistsException, UserNotFoundException
from core.utils.repository import AbstractRepository
from schemas.users import UserOut, UserCreate


class UserService:
    def __init__(self, user_repo_factory: Callable[[], AbstractRepository]):
        self.user_repo = user_repo_factory()

    async def create_user(self, user: UserCreate) -> int:
        existing_user = await self.user_repo.find_one_by_field('email', user.email)
        if existing_user:
            raise UserAlreadyExistsException('email', user.email)

        existing_user = await self.user_repo.find_one_by_field('username', user.username)
        if existing_user:
            raise UserAlreadyExistsException('username', user.username)

        user_dict = user.model_dump()
        user_id = await self.user_repo.create_one(user_dict)
        return user_id

    async def get_user_by_id(self, user_id: int) -> UserOut:
        user = await self.user_repo.find_one_by_id(user_id)
        if not user:
            raise UserNotFoundException('id', str(user_id))
        return user.to_read_model()

    async def get_users(self) -> list[UserOut]:
        users = await self.user_repo.find_all()
        return [user.to_read_model() for user in users]

    async def delete_user(self, user_id: int) -> None:
        user = await self.user_repo.find_one_by_id(user_id)
        if not user:
            raise UserNotFoundException('id', str(user_id))
        await self.user_repo.delete_one(user)

    async def get_user_by_email(self, email: str) -> UserOut:
        user = await self.user_repo.find_one_by_field('email', email)
        if not user:
            raise UserNotFoundException('email', email)
        return user.to_read_model()

    async def get_user_by_username(self, username: str) -> UserOut:
        user = await self.user_repo.find_one_by_field('username', username)
        if not user:
            raise UserNotFoundException('username', username)
        return user.to_read_model()
