from typing import Callable

from schemas.rounds.rounds import RoundOut
from services.rounds import RoundService
from use_cases.base import BaseUseCase


class GetCurrentRoundUseCase(BaseUseCase[None, RoundOut]):
    def __init__(self, round_service_factory: Callable[[], RoundService]):
        self.round_service = round_service_factory()

    async def execute(self, input_data: None = None) -> RoundOut:
        current_round = await self.round_service.get_current_round()
        return current_round.to_read_model(include_bets=True)
