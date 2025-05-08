from datetime import timezone, datetime, timedelta
from random import choices
from typing import Callable

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from core.exceptions import ItemAlreadyExistsException, ItemNotFoundException, InvalidFieldValueException
from core.utils.repository import AbstractRepository
from db.models import Bet
from db.models.rounds import Round
from schemas.rounds.rounds import RoundCreate, RoundStatus


class RoundService:
    def __init__(
            self,
            round_repo_factory: Callable[[], AbstractRepository],
    ):
        self._round_repo = round_repo_factory()

    async def _handle_foreign_key_not_found_violation(
            self, field: str, value: str,
    ):
        raise ItemNotFoundException("SneakerModel", field, value)

    async def create_round(self, round_to_create: RoundCreate) -> Round:
        current_time = datetime.now(timezone.utc)
        # TODO: less than 1 day
        if (round_to_create.planned_time.astimezone(
                timezone.utc) - current_time).total_seconds() <= 10:  # 86400 secs = 1 day
            raise InvalidFieldValueException("Round.planned_time", "planned time must be in the future")

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

    async def get_current_round(self, include_user: bool = False) -> Round:
        filters = [Round.status == RoundStatus.PLANNED]
        options = [selectinload(Round.bets).selectinload(Bet.user) if include_user else selectinload(Round.bets)]

        current_round = await self._round_repo.find_all_with_filters(
            filters=filters,
            limit=1,
            options=options
        )
        if not current_round:
            raise ItemNotFoundException("Round", "status", "planned")

        return current_round[0]

    async def close_round(self, round_id: int, winner_id: int) -> Round:
        prize_expires = datetime.now(timezone.utc) + timedelta(days=3)
        update_data = {
            "prize_expires_at": prize_expires,
            "status": RoundStatus.FINISHED,
            "winner_id": winner_id,
        }
        updated_round = await self._round_repo.update_one(round_id, update_data)
        return updated_round

    async def choose_current_round_winner(self) -> (Bet, Round):
        round = await self.get_current_round(include_user=True)
        if not round.bets:
            raise InvalidFieldValueException("Round.bets", "at least one bet to close the round")

        weights = [bet.amount for bet in round.bets]
        winner_bet = choices(round.bets, weights=weights, k=1)[0]
        return winner_bet, round
