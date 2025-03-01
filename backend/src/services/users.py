from typing import Callable

from fastapi import BackgroundTasks
from pydantic import EmailStr

from core.exceptions import UserAlreadyExistsException, UserNotFoundException, UserAlreadyVerifiedException, \
    UnverifiedEmailException
from core.utils.password import get_password_hash
from core.utils.repository import AbstractRepository
from services.email import EmailService
from db.models.users import User
from schemas.users import UserOut, UserCreate
from services.jwt import TokenService


class UserService:
    def __init__(self, user_repo_factory: Callable[[], AbstractRepository]):
        self.user_repo = user_repo_factory()
        self.token_service = TokenService()
        self.email_service = EmailService()

    async def create_user(self, user: UserCreate, background_tasks: BackgroundTasks) -> int:
        existing_user = await self.user_repo.find_one_by_field('email', user.email)
        if existing_user:
            raise UserAlreadyExistsException('email', user.email)

        existing_user = await self.user_repo.find_one_by_field('username', user.username)
        if existing_user:
            raise UserAlreadyExistsException('username', user.username)
        user_dict = user.model_dump()
        user_dict["password"] = get_password_hash(user_dict["password"])
        user_id = await self.user_repo.create_one(user_dict)

        token = self.token_service.create_verification_token(User(**user_dict))
        background_tasks.add_task(self.email_service.send_verification_email, user.email, token)

        return user_id

    async def verify_email(self, token: str) -> None:
        try:
            payload = self.token_service.verify_token(token)
            user = await self.user_repo.find_one_by_field('username', payload["sub"])
            if not user:
                raise UserNotFoundException('username', payload["sub"])
            if user.is_verified:
                raise UserAlreadyVerifiedException(str(user.id))
            await self.user_repo.update_one(user, {"is_verified": True})
        except ValueError:
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

    async def update_user_email(self, user_id: int, new_email: EmailStr, background_tasks: BackgroundTasks) -> UserOut:
        existing_user = await self.user_repo.find_one_by_field('email', new_email)
        if existing_user:
            raise UserAlreadyExistsException('email', new_email)

        user = await self.user_repo.find_one_by_id(user_id)
        if not user:
            raise UserNotFoundException('id', str(user_id))
        if not user.is_verified:
            raise UnverifiedEmailException()

        updated_user = await self.user_repo.update_one(user, {"email": new_email, "is_verified": False})

        token = self.token_service.create_verification_token(user)
        background_tasks.add_task(self.email_service.send_verification_email, user.email, token)

        return updated_user.to_read_model()

    async def update_user_username(self, user_id: int, new_username: str) -> UserOut:
        existing_user = await self.user_repo.find_one_by_field('username', new_username)
        if existing_user:
            raise UserAlreadyExistsException('username', new_username)

        user = await self.user_repo.find_one_by_id(user_id)
        if not user:
            raise UserNotFoundException('id', str(user_id))
        if not user.is_verified:
            raise UnverifiedEmailException()

        updated_user = await self.user_repo.update_one(user, {"username": new_username})

        return updated_user.to_read_model()

    async def request_password_reset(self, email: EmailStr, background_tasks: BackgroundTasks) -> None:
        user = await self.user_repo.find_one_by_field('email', email)
        if not user:
            raise UserNotFoundException('email', email)
        if not user.is_verified:
            raise UnverifiedEmailException()

        token = self.token_service.create_verification_token(user)
        background_tasks.add_task(self.email_service.send_change_password_email, user.email, token)

    async def update_password(self, token: str, new_password: str):
        try:
            payload = self.token_service.verify_token(token)
            user = await self.user_repo.find_one_by_field('username', payload["sub"])
            if not user:
                raise UserNotFoundException('username', payload["sub"])
            if not user.is_verified:
                raise UnverifiedEmailException()

            new_hashed_password = get_password_hash(new_password)
            await self.user_repo.update_one(user, {"password": new_hashed_password})
        except ValueError:
            raise ValueError("Invalid verification token")
