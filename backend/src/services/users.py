from typing import Callable, Any

from pydantic import EmailStr
from sqlalchemy.exc import IntegrityError

from core.exceptions import (
    ItemAlreadyExistsException,
    ItemNotFoundException,
    UserAlreadyVerifiedException,
    InvalidCredentialsException,
    UnverifiedEmailException,
)
from core.utils.password import get_password_hash, verify_password
from core.utils.repository import AbstractRepository
from db.models.users import User
from schemas.users.users import UserCreate


class UserService:
    def __init__(self, user_repo_factory: Callable[[], AbstractRepository]):
        self._user_repo = user_repo_factory()

    async def _handle_unique_violation(
            self, fields: dict[str, Any],
    ):
        raise ItemAlreadyExistsException("User", fields)

    async def create_user(self, user: UserCreate) -> User:
        user_dict = user.model_dump()
        user_dict["password"] = get_password_hash(user_dict["password"])

        try:
            created_user = await self._user_repo.create_one(user_dict)
        except IntegrityError as e:
            if "unique constraint" in str(e).lower():
                if "email" in str(e).lower():
                    await self._handle_unique_violation({"email": user.email})
                elif "username" in str(e).lower():
                    await self._handle_unique_violation({"username": user.username})
            raise

        return created_user

    async def get_user_by_email(self, email: EmailStr) -> User:
        user = await self._user_repo.find_one_by_field(email=email)
        if not user:
            raise ItemNotFoundException("User", "email", email)
        return user

    async def get_verified_user_by_email(self, email: EmailStr) -> User:
        user = await self.get_user_by_email(email)
        if not user.is_verified:
            raise UnverifiedEmailException()
        return user

    async def get_user_by_username(self, username: str) -> User:
        user = await self._user_repo.find_one_by_field(username=username)
        if not user:
            raise ItemNotFoundException("User", "username", username)
        return user

    async def update_user_verification(self, user: User, is_verified: bool) -> User:
        if is_verified and user.is_verified:
            raise UserAlreadyVerifiedException(str(user.id))

        return await self._user_repo.update_one(user.id, {"is_verified": is_verified})

    async def get_user_by_id(self, user_id: int) -> User:
        user = await self._user_repo.find_one_by_field(id=user_id)
        if not user:
            raise ItemNotFoundException("User", "id", str(user_id))
        return user

    async def delete_user(self, user_id: int) -> None:
        success = await self._user_repo.delete_one(user_id)
        if not success:
            raise ItemNotFoundException("User", "id", str(user_id))

    async def update_user_email(self, user_id: int, new_email: EmailStr) -> User:
        try:
            updated_user = await self._user_repo.update_one(
                user_id,
                {"email": new_email, "is_verified": False},
            )
        except IntegrityError as e:
            if "unique constraint" in str(e).lower():
                await self._handle_unique_violation({"email": new_email})
            raise

        return updated_user

    async def update_user_username(self, user_id: int, new_username: str) -> User:
        try:
            updated_user = await self._user_repo.update_one(
                user_id,
                {"username": new_username},
            )
        except IntegrityError as e:
            if "unique constraint" in str(e).lower():
                await self._handle_unique_violation({"username": new_username})
            raise

        return updated_user

    async def update_user_password(self, user_id: int, new_password: str) -> User:
        hashed_password = get_password_hash(new_password)
        return await self._user_repo.update_one(user_id, {"password": hashed_password})

    async def change_password(
            self, user_id: int, current_password: str, new_password: str
    ) -> None:
        user = await self.get_user_by_id(user_id)

        if not verify_password(current_password, user.password):
            raise InvalidCredentialsException()

        await self.update_user_password(user_id, new_password)
