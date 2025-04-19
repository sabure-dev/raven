from typing import Callable, Any

from sqlalchemy.exc import IntegrityError

from core.exceptions import ItemNotFoundException, ItemAlreadyExistsException, InvalidFieldValueException
from core.utils.repository import AbstractRepository
from db.models import Bet
from schemas.bets.bets import BetCreate
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
