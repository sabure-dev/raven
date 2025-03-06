from typing import Callable, List

from schemas.use_cases import GetUserInput
from schemas.users import UserOut
from services.users import UserService
from use_cases.base import BaseUseCase


class GetUserUseCase(BaseUseCase[GetUserInput, UserOut]):
    def __init__(self, user_service_factory: Callable[[], UserService]):
        self.user_service = user_service_factory()

    async def execute(self, input_data: GetUserInput) -> UserOut:
        return await self.user_service.get_user_by_id(input_data.user_id)


class GetUsersUseCase(BaseUseCase[None, List[UserOut]]):
    def __init__(self, user_service_factory: Callable[[], UserService]):
        self.user_service = user_service_factory()

    async def execute(self, input_data: None = None) -> List[UserOut]:
        return await self.user_service.get_users()
