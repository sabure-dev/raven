from typing import Callable

from schemas.bets.bets import BetOut
from schemas.bets.use_cases import CreateBetInput
from services.bets import BetService
from services.users import UserService
from use_cases.base import BaseUseCase


class CreateBetUseCase(BaseUseCase[CreateBetInput, BetOut]):
    def __init__(
            self,
            bet_service_factory: Callable[[], BetService],
            user_service_factory: Callable[[], UserService],
    ):
        self.bet_service = bet_service_factory()
        self.user_service = user_service_factory()

    async def execute(self, input_data: CreateBetInput) -> BetOut:
        created_bet = await self.bet_service.create_bet(
            input_data.bet,
            input_data.user_id,
        )

        await self.user_service.update_balance_after_bet(
            input_data.user_id,
            -input_data.bet.amount,
        )

        return created_bet.to_read_model()
