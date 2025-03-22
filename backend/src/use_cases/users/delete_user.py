from typing import Callable

from schemas.users.use_cases import DeleteUserInput
from services.users import UserService
from use_cases.base import BaseUseCase


class DeleteUserUseCase(BaseUseCase[DeleteUserInput, None]):
    def __init__(self, user_service_factory: Callable[[], UserService]):
        self.user_service = user_service_factory()

    async def execute(self, input_data: DeleteUserInput) -> None:
        await self.user_service.delete_user(input_data.user_id)
