from typing import Callable

from schemas.users.use_cases import GetUserInput
from schemas.users.users import UserOut
from services.users import UserService
from use_cases.base import BaseUseCase


class GetUserUseCase(BaseUseCase[GetUserInput, UserOut]):
    def __init__(self, user_service_factory: Callable[[], UserService]):
        self.user_service = user_service_factory()

    async def execute(self, input_data: GetUserInput) -> UserOut:
        user = await self.user_service.get_user_by_id(input_data.user_id, load_orders=True)
        return user.to_read_model(include_orders=True)
