from typing import Callable

from fastapi import Depends

from core.dependencies.rounds.database import (
    get_round_repository_factory,
)
from repositories.rounds import RoundRepository
from services.rounds import RoundService


def get_round_service_factory(
        round_repository_factory: Callable[[], RoundRepository] = Depends(
            get_round_repository_factory
        ),
) -> Callable[[], RoundService]:
    return lambda: RoundService(round_repository_factory)
