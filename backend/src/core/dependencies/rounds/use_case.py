from typing import Callable

from fastapi import Depends

from core.dependencies.rounds.services import get_round_service_factory
from services.rounds import RoundService
from use_cases.rounds.create_round import CreateRoundUseCase
from use_cases.rounds.get_current_round import GetCurrentRoundUseCase


def get_create_round_use_case(
        round_service_factory: Callable[[], RoundService] = Depends(
            get_round_service_factory
        ),
) -> CreateRoundUseCase:
    return CreateRoundUseCase(round_service_factory)


def get_get_current_round_use_case(
        round_service_factory: Callable[[], RoundService] = Depends(
            get_round_service_factory
        ),
) -> GetCurrentRoundUseCase:
    return GetCurrentRoundUseCase(round_service_factory)
