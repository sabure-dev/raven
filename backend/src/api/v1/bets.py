from fastapi import APIRouter, Depends

from core.dependencies.bets.use_cases import get_create_bet_use_case
from core.dependencies.users.security import get_current_superuser, get_current_active_verified_user
from db.models import User
from schemas.bets.bets import BetOut, BetCreate
from schemas.bets.use_cases import CreateBetInput

router = APIRouter(prefix="/bets",
                   tags=["Bets"])


@router.post("", response_model=BetOut)
async def create_bet(
        bet_to_create: BetCreate,
        create_bet_use_case=Depends(get_create_bet_use_case),
        user: User = Depends(get_current_active_verified_user),
):
    created_bet = await create_bet_use_case.execute(
        CreateBetInput(bet=bet_to_create, user_id=user.id)
    )
    return created_bet
