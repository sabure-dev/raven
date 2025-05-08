from core.dependencies.rounds.delayed_task_use_case import get_close_round_use_case
from core.tasks.task_app import broker
from taskiq import TaskiqDepends


@broker.task
async def delay_close_round_task(close_round_use_case=TaskiqDepends(
    get_close_round_use_case
)):
    await close_round_use_case.execute()
