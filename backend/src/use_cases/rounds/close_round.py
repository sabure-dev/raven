from typing import Callable

from fastapi import BackgroundTasks

from services.bets import BetService
from services.email import EmailService
from services.rounds import RoundService
from use_cases.base import BaseUseCase


class CloseRoundUseCase(BaseUseCase[None, None]):
    def __init__(
            self,
            round_service_factory: Callable[[], RoundService],
            bet_service_factory: Callable[[], BetService],
            email_service_factory: Callable[[], EmailService],
            background_tasks: BackgroundTasks,
    ):
        self.round_service = round_service_factory()
        self.bet_service = bet_service_factory()
        self.email_service = email_service_factory()
        self.background_tasks = background_tasks

    async def execute(self, input_data: None = None) -> None:
        round_winner, current_round = await self.round_service.choose_current_round_winner()

        await self.round_service.close_round(current_round.id, round_winner.user_id)
        self.background_tasks.add_task(
            self.email_service.send_prize_email, round_winner.user.email
        )

        # TODO: добавить выдачу призов в отдельном юз кейсе через эндпоинт (бесплатный заказ)
        # order = await self.order_service.create_order(
        #     OrderCreate(total_amount=0),
        #     user_id=round_winner.user_id,
        # )
        # order_item = self.order_item_service.create_order_item(
        #     OrderItemCreateInDB(
        #         quantity=,
        #         sneaker_variant_id=,
        #         price_at_time=0,
        #         order_id=order.id,
        #     )
        # )


