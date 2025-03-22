from typing import Callable, List

from pydantic import EmailStr
from sqlalchemy.exc import IntegrityError

from core.exceptions import ItemAlreadyExistsException, ItemNotFoundException, UserAlreadyVerifiedException, \
    InvalidCredentialsException, UnverifiedEmailException
from core.utils.password import get_password_hash, verify_password
from core.utils.repository import AbstractRepository
from db.models.users import User
from schemas.users.users import UserCreate


class UserService:
    def __init__(self, user_repo_factory: Callable[[], AbstractRepository]):
        self.user_repo = user_repo_factory()

    async def _handle_unique_violation(self, error: IntegrityError, field: str, value: str):
        if "unique constraint" in str(error).lower():
            raise ItemAlreadyExistsException('User', field, value)
        raise

    async def create_user(self, user: UserCreate) -> (int, User):
        user_dict = user.model_dump()
        user_dict["password"] = get_password_hash(user_dict["password"])

        try:
            user_id = await self.user_repo.create_one(user_dict)
        except IntegrityError as e:
            if 'email' in str(e).lower():
                await self._handle_unique_violation(e, 'email', user.email)
            elif 'username' in str(e).lower():
                await self._handle_unique_violation(e, 'username', user.username)
            raise

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

    # TODO: add search by filters like with sneakers
    async def get_users(self) -> List[User]:
        return await self.user_repo.find_all()

    async def delete_user(self, user_id: int) -> None:
        user = await self.get_user_by_id(user_id)
        await self.user_repo.delete_one(user)

    async def update_user_email(self, user_id: int, new_email: EmailStr) -> User:
        user = await self.get_user_by_id(user_id)
        try:
            updated_user = await self.user_repo.update_one(
                user,
                {'email': new_email, 'is_verified': False},
            )
        except IntegrityError as e:
            await self._handle_unique_violation(e, 'email', new_email)
            raise

        return updated_user

    async def update_user_username(self, user_id: int, new_username: str) -> User:
        user = await self.get_user_by_id(user_id)
        try:
            updated_user = await self.user_repo.update_one(
                user,
                {'username': new_username},
            )
        except IntegrityError as e:
            await self._handle_unique_violation(e, 'username', new_username)
            raise

        return updated_user

    async def update_user_password(self, user: User, new_password: str) -> User:
        hashed_password = get_password_hash(new_password)
        return await self.user_repo.update_one(user, {'password': hashed_password})

    async def change_password(self, user_id: int, current_password: str, new_password: str) -> None:
        user = await self.get_user_by_id(user_id)

        if not verify_password(current_password, user.password):
            raise InvalidCredentialsException()

        await self.update_user_password(user, new_password)
