from typing import Callable, Optional, List

from pydantic import EmailStr

from core.exceptions import UserAlreadyExistsException, UserNotFoundException, UserAlreadyVerifiedException, \
    UnverifiedEmailException
from core.utils.password import get_password_hash
from core.utils.repository import AbstractRepository
from db.models.users import User
from schemas.users import UserOut, UserCreate


class UserService:
    def __init__(self, user_repo_factory: Callable[[], AbstractRepository]):
        self.user_repo = user_repo_factory()

    async def create_user(self, user: UserCreate) -> (int, User):
        existing_user = await self.user_repo.find_one_by_field('email', user.email)
        if existing_user:
            raise UserAlreadyExistsException('email', user.email)

        existing_user = await self.user_repo.find_one_by_field('username', user.username)
        if existing_user:
            raise UserAlreadyExistsException('username', user.username)

        user_dict = user.model_dump()
        user_dict["password"] = get_password_hash(user_dict["password"])
        user_id = await self.user_repo.create_one(user_dict)

        created_user = User(**user_dict)
        created_user.id = user_id

        return user_id, created_user

    async def get_user_by_username(self, username: str) -> User:
        user = await self.user_repo.find_one_by_field('username', username)
        if not user:
            raise UserNotFoundException('username', username)
        return user

    async def update_user_verification(self, user: User, is_verified: bool) -> User:
        if is_verified and user.is_verified:
            raise UserAlreadyVerifiedException(str(user.id))

        return await self.user_repo.update_one(user, {'is_verified': is_verified})

    async def get_user_by_id(self, user_id: int) -> Optional[UserOut]:
        user = await self.user_repo.find_one_by_id(user_id)
        if not user:
            raise UserNotFoundException("id", str(user_id))
        return user.to_read_model()

    async def get_users(self) -> List[UserOut]:
        users = await self.user_repo.find_all()
        return [user.to_read_model() for user in users]

    async def delete_user(self, user_id: int) -> None:
        user = await self.user_repo.find_one_by_id(user_id)
        if not user:
            raise UserNotFoundException("id", str(user_id))
        await self.user_repo.delete_one(user)

    async def update_user_email(self, user_id: int, new_email: EmailStr) -> User:
        user = await self.user_repo.find_one_by_id(user_id)
        if not user:
            raise UserNotFoundException("id", str(user_id))

        existing_user = await self.user_repo.find_one_by_field('email', new_email)
        if existing_user:
            raise UserAlreadyExistsException('email', new_email)

        return await self.user_repo.update_one(user, {'email': new_email, 'is_verified': False})

    async def update_user_username(self, user_id: int, new_username: str) -> UserOut:
        user = await self.user_repo.find_one_by_id(user_id)
        if not user:
            raise UserNotFoundException("id", str(user_id))

        if not user.is_verified:
            raise UnverifiedEmailException()

        existing_user = await self.user_repo.find_one_by_field('username', new_username)
        if existing_user:
            raise UserAlreadyExistsException('username', new_username)

        updated_user = await self.user_repo.update_one(user, {'username': new_username})

        return updated_user.to_read_model()

    async def get_user_by_email(self, email: EmailStr) -> User:
        user = await self.user_repo.find_one_by_field('email', email)
        if not user:
            raise UserNotFoundException('email', email)
        return user

    async def update_user_password(self, user: User, new_password: str) -> User:
        hashed_password = get_password_hash(new_password)
        return await self.user_repo.update_one(user, {'password': hashed_password})
