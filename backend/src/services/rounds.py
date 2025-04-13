from typing import Callable, Literal

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
        existing_coworking = await self._round_repo.find_one_by_field(status=RoundStatus.PLANNED)
        if existing_coworking:
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
        order_by: tuple[str, Literal["asc", "desc"]] = ("id", "desc")
        options = [selectinload(Round.bets)]

        current_round = await self._round_repo.find_all_with_filters(
            filters=filters,
            limit=1,
            order_by=order_by,
            options=options
        )
        if current_round is None:
            raise ItemNotFoundException("Round", "status", "planned")

        return current_round[0]
