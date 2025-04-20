from typing import Callable

from schemas.bets.bets import BetOut
from schemas.bets.use_cases import IncreaseBetAmountInput
from services.bets import BetService
from use_cases.base import BaseUseCase


# TODO: add decrease balance after increase
class IncreaseBetAmountUseCase(BaseUseCase[IncreaseBetAmountInput, BetOut]):
    def __init__(
            self,
            bet_service_factory: Callable[[], BetService],
    ):
        self.bet_service = bet_service_factory()

    async def execute(self, input_data: IncreaseBetAmountInput) -> BetOut:
        updated_bet = await self.bet_service.increase_user_bet_amount(
            input_data.delta,
            input_data.user_id,
        )
        return updated_bet.to_read_model()
