from typing import Callable

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from core.exceptions import ItemAlreadyExistsException, ItemNotFoundException
from core.utils.repository import AbstractRepository
from db.models.rounds import Round
from schemas.rounds.rounds import RoundCreate, RoundStatus


class RoundService:
    def __init__(self, round_repo_factory: Callable[[], AbstractRepository]):
        self._round_repo = round_repo_factory()

    async def _handle_foreign_key_not_found_violation(
            self, field: str, value: str,
    ):
        raise ItemNotFoundException("SneakerModel", field, value)

    async def create_round(self, round_to_create: RoundCreate) -> Round:
        round_dict = round_to_create.model_dump()
        existing_round = await self._round_repo.find_one_by_fields(filters=(Round.status == RoundStatus.PLANNED))
        if existing_round:
            raise ItemAlreadyExistsException("Round", {"status": RoundStatus.PLANNED})
        try:
            created_round = await self._round_repo.create_one(round_dict)
        except IntegrityError as e:
            if "foreign key" in str(e).lower():
                await self._handle_foreign_key_not_found_violation("id", str(round_to_create.model_id))
            raise
        return created_round

    async def get_current_round(self) -> Round:
        filters = [Round.status == RoundStatus.PLANNED]
        options = [selectinload(Round.bets)]

        current_round = await self._round_repo.find_all_with_filters(
            filters=filters,
            limit=1,
            options=options
        )
        if not current_round:
            raise ItemNotFoundException("Round", "status", "planned")

        return current_round[0]

    async def close_current_round(self) -> None:
        round = await self.get_current_round()

        update_data = {
            "status": RoundStatus.FINISHED,
        }
        updated_round = await self._round_repo.update_one(round.id, update_data)
        # TODO: add winner selection logic

        return updated_round
