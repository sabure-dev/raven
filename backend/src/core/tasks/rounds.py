from typing import Callable

from core.dependencies.rounds.services import get_round_service_factory
from core.tasks.task_app import broker
from taskiq import TaskiqDepends

from services.rounds import RoundService


@broker.task
async def delay_close_round_task(round_service_factory: Callable[[], RoundService] = TaskiqDepends(
    get_round_service_factory
)):
    round_service = round_service_factory()
    await round_service.close_current_round()
