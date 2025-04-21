from typing import Callable

from schemas.bets.bets import BetOut
from schemas.bets.use_cases import GetUserBetsInput
from services.bets import BetService
from use_cases.base import BaseUseCase


class GetUserBetsUseCase(BaseUseCase[GetUserBetsInput, list[BetOut]]):
    def __init__(
            self, bet_service_factory: Callable[[], BetService]
    ):
        self.bet_service = bet_service_factory()

    async def execute(
            self, input_data: GetUserBetsInput
    ) -> list[BetOut]:
        bets = await self.bet_service.get_user_bets(
            user_id=input_data.user_id,
            is_winner=input_data.params.is_winner,
            is_actual=input_data.params.is_actual,
            offset=input_data.params.offset,
            limit=input_data.params.limit,
            sort_by_date=input_data.params.sort_by_date,
        )
        return [bet.to_read_model() for bet in bets]
