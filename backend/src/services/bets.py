from typing import Callable, Any

from sqlalchemy.exc import IntegrityError

from core.exceptions import ItemNotFoundException, ItemAlreadyExistsException
from core.utils.repository import AbstractRepository
from db.models import Bet
from schemas.bets.bets import BetCreate


class BetService:
    def __init__(self, bet_repo_factory: Callable[[], AbstractRepository]):
        self._bet_repo = bet_repo_factory()

    async def _handle_unique_violation(
            self, fields: dict[str, Any],
    ):
        raise ItemAlreadyExistsException("Bet", fields)

    async def _handle_foreign_key_not_found_violation(
            self, item: str, field: str, value: str,
    ):
        raise ItemNotFoundException(item, field, value)

    async def create_bet(self, bet_to_create: BetCreate, user_id: int) -> Bet:
        bet_dict = bet_to_create.model_dump()
        try:
            bet_id = await self._bet_repo.create_one(bet_dict)
        except IntegrityError as e:
            if "foreign key" in str(e).lower():
                if "user_id" in str(e).lower():
                    await self._handle_foreign_key_not_found_violation("User", "id", str(user_id))
                if "round_id" in str(e).lower():
                    await self._handle_foreign_key_not_found_violation("Round", "id", str(bet_to_create.round_id))

            elif "unique constraint" in str(e).lower():
                await self._handle_unique_violation({
                    "round_id": bet_to_create.round_id,
                    "user_id": user_id,
                })
            raise
        return bet_id
