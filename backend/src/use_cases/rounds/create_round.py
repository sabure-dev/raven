from datetime import datetime, timezone, timedelta
from typing import Callable

from schemas.rounds.rounds import RoundOut
from schemas.rounds.use_cases import CreateRoundInput
from services.rounds import RoundService
from use_cases.base import BaseUseCase
from core.tasks.rounds import delay_close_round_task


class CreateRoundUseCase(BaseUseCase[CreateRoundInput, RoundOut]):
    def __init__(
            self,
            round_service_factory: Callable[[], RoundService],
    ):
        self.round_service = round_service_factory()

    async def execute(self, input_data: CreateRoundInput) -> RoundOut:
        created_round = await self.round_service.create_round(
            input_data.round
        )

        current_time = datetime.now(timezone.utc)
        delay_seconds = (
            input_data.round.planned_time.astimezone(timezone.utc) - current_time
        ).total_seconds()

        await delay_close_round_task.kicker().with_labels(delay=delay_seconds).kiq()
        return created_round.to_read_model()
