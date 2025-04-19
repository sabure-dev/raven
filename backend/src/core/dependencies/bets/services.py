from typing import Callable

from fastapi import Depends

from core.dependencies.bets.database import (
    get_bet_repository_factory,
)
from core.dependencies.rounds.services import get_round_service_factory
from repositories.bets import BetRepository
from services.bets import BetService
from services.rounds import RoundService


def get_bet_service_factory(
        bet_repository_factory: Callable[[], BetRepository] = Depends(
            get_bet_repository_factory
        ),
        round_service_factory: Callable[[], RoundService] = Depends(
            get_round_service_factory
        )
) -> Callable[[], BetService]:
    return lambda: BetService(bet_repository_factory, round_service_factory)
