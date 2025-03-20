from typing import Callable, List

from pydantic import EmailStr

from core.exceptions import ItemAlreadyExistsException, ItemNotFoundException, UserAlreadyVerifiedException, \
    InvalidCredentialsException, UnverifiedEmailException
from core.utils.password import get_password_hash, verify_password
from core.utils.repository import AbstractRepository
from db.models.users import User
from schemas.users import UserCreate


class UserService:
    def __init__(self, user_repo_factory: Callable[[], AbstractRepository]):
        self.user_repo = user_repo_factory()

    async def _check_field_unique(self, field_name: str, value: str):
        existing_user = await self.user_repo.find_one_by_field(field_name, value)
        if existing_user:
            raise ItemAlreadyExistsException('User', field_name, value)

    async def create_user(self, user: UserCreate) -> (int, User):
        await self._check_field_unique('email', user.email)
        await self._check_field_unique('username', user.username)

        user_dict = user.model_dump()
        user_dict["password"] = get_password_hash(user_dict["password"])
        user_id = await self.user_repo.create_one(user_dict)

        created_user = User(**user_dict)
        created_user.id = user_id

        return user_id, created_user

    async def get_user_by_email(self, email: EmailStr) -> User:
        user = await self.user_repo.find_one_by_field('email', email)
        if not user:
            raise ItemNotFoundException('User', 'email', email)
        return user

    async def get_verified_user_by_email(self, email: EmailStr) -> User:
        user = await self.get_user_by_email(email)
        if not user.is_verified:
            raise UnverifiedEmailException()
        return user

    async def get_user_by_username(self, username: str) -> User:
        user = await self.user_repo.find_one_by_field('username', username)
        if not user:
            raise ItemNotFoundException('User', 'username', username)
        return user

    async def update_user_verification(self, user: User, is_verified: bool) -> User:
        if is_verified and user.is_verified:
            raise UserAlreadyVerifiedException(str(user.id))

        return await self.user_repo.update_one(user, {'is_verified': is_verified})

    async def get_user_by_id(self, user_id: int) -> User:
        user = await self.user_repo.find_one_by_id(user_id)
        if not user:
            raise ItemNotFoundException('User', "id", str(user_id))
        return user

    async def get_users(self) -> List[User]:
        return await self.user_repo.find_all()

    async def delete_user(self, user_id: int) -> None:
        user = await self.get_user_by_id(user_id)
        await self.user_repo.delete_one(user)

    async def update_user_email(self, user_id: int, new_email: EmailStr) -> User:
        user = await self.get_user_by_id(user_id)
        await self._check_field_unique('email', new_email)

        return await self.user_repo.update_one(user, {'email': new_email, 'is_verified': False})

    async def update_user_username(self, user_id: int, new_username: str) -> User:
        user = await self.get_user_by_id(user_id)
        await self._check_field_unique('username', new_username)

        return await self.user_repo.update_one(user, {'username': new_username})

    async def update_user_password(self, user: User, new_password: str) -> User:
        hashed_password = get_password_hash(new_password)
        return await self.user_repo.update_one(user, {'password': hashed_password})

    async def change_password(self, user_id: int, current_password: str, new_password: str) -> None:
        user = await self.get_user_by_id(user_id)

        if not verify_password(current_password, user.password):
            raise InvalidCredentialsException()

        await self.update_user_password(user, new_password)
