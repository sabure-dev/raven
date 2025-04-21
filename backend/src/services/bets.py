from typing import Callable, Any, Literal

from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from core.exceptions import ItemNotFoundException, ItemAlreadyExistsException, InvalidFieldValueException
from core.utils.repository import AbstractRepository
from db.models import Bet, Round
from schemas.bets.bets import BetCreate
from schemas.rounds.rounds import RoundStatus
from services.rounds import RoundService


class BetService:
    def __init__(self,
                 bet_repo_factory: Callable[[], AbstractRepository],
                 round_service_factory: Callable[[], RoundService],
                 ):
        self._bet_repo = bet_repo_factory()
        self._round_service = round_service_factory()

    async def _handle_unique_violation(
            self, fields: dict[str, Any],
    ):
        raise ItemAlreadyExistsException("Bet", fields)

    async def _handle_foreign_key_not_found_violation(
            self, item: str, field: str, value: str,
    ):
        raise ItemNotFoundException(item, field, value)

    async def _validate_bet_amount(
            self, min_bet_amount: int, amount: float
    ):
        if amount < min_bet_amount:
            raise InvalidFieldValueException("Bet.amount",
                                             f'must be greater or equal to min_bet_amount ({min_bet_amount})')

    async def create_bet(self, bet_to_create: BetCreate, user_id: int) -> Bet:
        round = await self._round_service.get_current_round()
        await self._validate_bet_amount(round.min_bet_amount, bet_to_create.amount)

        bet_dict = bet_to_create.model_dump()
        bet_dict["user_id"] = user_id
        bet_dict["round_id"] = round.id

        try:
            created_bet = await self._bet_repo.create_one(bet_dict)
        except IntegrityError as e:
            if "foreign key" in str(e).lower():
                if "bets_user_id_fkey" in str(e).lower():
                    await self._handle_foreign_key_not_found_violation("User", "id", str(user_id))
                if "bets_round_id_fkey" in str(e).lower():
                    await self._handle_foreign_key_not_found_violation("Round", "id", str(round.id))

            elif "unique constraint" in str(e).lower():
                await self._handle_unique_violation({
                    "round_id": round.id,
                    "user_id": user_id,
                })
            raise
        return created_bet

    # TODO: add is_actual
    async def get_user_bets(
            self,
            user_id: int,
            is_winner: bool = False,
            offset: int | None = None,
            limit: int | None = None,
            sort_by_date: Literal["asc", "desc"] | None = None
    ) -> list[Bet]:
        filters = [Bet.user_id == user_id]
        options = [joinedload(Bet.round)]
        order_by = ("created_at", sort_by_date) if sort_by_date else None

        if is_winner:
            filters.append(Bet.is_winner == is_winner)

        bets = await self._bet_repo.find_all_with_filters(
            filters=filters,
            options=options,
            order_by=order_by,
            offset=offset,
            limit=limit,
        )

        return bets

    async def increase_bet_amount(self, delta: float, bet_id: int) -> Bet:
        updated_bet = await self._bet_repo.increment_field(
            bet_id,
            "amount",
            delta,
        )

        if updated_bet is None:
            raise ItemNotFoundException("Bet", "id", str(bet_id))

        return updated_bet

    async def increase_user_bet_amount(self, delta: float, user_id: int) -> Bet:
        result = await self._bet_repo.find_one_by_fields(
            fields_to_return=[Bet, Round.min_bet_amount],
            joins=[Round],
            filters=and_(
                Bet.user_id == user_id,
                Round.status == RoundStatus.PLANNED
                ),
        )
        if not result:
            raise ItemNotFoundException("Round", "status", "PLANNED")

        bet, min_bet_amount = result
        await self._validate_bet_amount(min_bet_amount, delta)

        updated_bet = await self.increase_bet_amount(delta, bet.id)
        return updated_bet
