from typing import Callable

from fastapi import Depends

from core.dependencies.bets.services import get_bet_service_factory
from core.dependencies.email.services import get_email_service_factory
from core.dependencies.rounds.services import get_round_service_factory
from services.bets import BetService
from services.email import EmailService
from services.rounds import RoundService
from use_cases.rounds.close_round import CloseRoundUseCase


def get_close_round_use_case(
        round_service_factory: Callable[[], RoundService] = Depends(
            get_round_service_factory
        ),
        bet_service_factory: Callable[[], BetService] = Depends(
            get_bet_service_factory,
        ),
        email_service_factory: Callable[[], EmailService] = Depends(
            get_email_service_factory,
        ),
) -> CloseRoundUseCase:
    return CloseRoundUseCase(round_service_factory, bet_service_factory, email_service_factory)
