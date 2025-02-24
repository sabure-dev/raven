from typing import Callable

from fastapi import BackgroundTasks

from core.exceptions import UserAlreadyExistsException, UserNotFoundException
from core.utils.repository import AbstractRepository
from core.utils.email import send_verification_email
from core.utils.token import create_verification_token, verify_token
from schemas.users import UserOut, UserCreate


class UserService:
    def __init__(self, user_repo_factory: Callable[[], AbstractRepository]):
        self.user_repo = user_repo_factory()

    async def create_user(self, user: UserCreate, background_tasks: BackgroundTasks) -> int:
        existing_user = await self.user_repo.find_one_by_field('email', user.email)
        if existing_user:
            raise UserAlreadyExistsException('email', user.email)

        existing_user = await self.user_repo.find_one_by_field('username', user.username)
        if existing_user:
            raise UserAlreadyExistsException('username', user.username)

        user_dict = user.model_dump()
        user_id = await self.user_repo.create_one(user_dict)

        token = create_verification_token(user.email)
        background_tasks.add_task(send_verification_email, user.email, token)

        return user_id

    async def verify_email(self, token: str) -> None:
        try:
            email = verify_token(token)
            user = await self.user_repo.find_one_by_field('email', email)
            if not user:
                raise UserNotFoundException('email', email)
            
            await self.user_repo.update_one(user, {"is_verified": True})
        except ValueError as e:
            raise ValueError("Invalid verification token")

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
