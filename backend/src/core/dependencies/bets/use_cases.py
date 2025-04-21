from typing import Callable

from fastapi import Depends

from core.dependencies.bets.services import get_bet_service_factory
from core.dependencies.users.services import get_user_service_factory
from services.bets import BetService
from services.users import UserService
from use_cases.bets.create_bet import CreateBetUseCase
from use_cases.bets.get_user_bets import GetUserBetsUseCase
from use_cases.bets.increase_bet_amount import IncreaseBetAmountUseCase


def get_create_bet_use_case(
        bet_service_factory: Callable[[], BetService] = Depends(
            get_bet_service_factory
        ),
        user_service_factory: Callable[[], UserService] = Depends(
            get_user_service_factory
        ),
) -> CreateBetUseCase:
    return CreateBetUseCase(bet_service_factory, user_service_factory)


def get_increase_bet_amount_use_case(
        bet_service_factory: Callable[[], BetService] = Depends(
            get_bet_service_factory
        ),
        user_service_factory: Callable[[], UserService] = Depends(
            get_user_service_factory
        ),
) -> IncreaseBetAmountUseCase:
    return IncreaseBetAmountUseCase(bet_service_factory, user_service_factory)


def get_get_user_bets_use_case(
        bet_service_factory: Callable[[], BetService] = Depends(
            get_bet_service_factory
        ),
) -> GetUserBetsUseCase:
    return GetUserBetsUseCase(bet_service_factory)
