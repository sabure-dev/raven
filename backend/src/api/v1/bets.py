from typing import Annotated

from fastapi import APIRouter, Depends, Query

from core.dependencies.bets.use_cases import get_create_bet_use_case, get_increase_bet_amount_use_case, \
    get_get_user_bets_use_case
from core.dependencies.users.security import get_current_active_verified_user
from db.models import User
from schemas.bets.bets import BetOut, BetCreate, BetParams
from schemas.bets.use_cases import CreateBetInput, IncreaseBetAmountInput, GetUserBetsInput

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


@router.patch("", response_model=BetOut)
async def increase_bet_amount(
        delta: Annotated[float, Query(gt=0)],
        increase_bet_amount_use_case=Depends(get_increase_bet_amount_use_case),
        user: User = Depends(get_current_active_verified_user),
):
    updated_bet = await increase_bet_amount_use_case.execute(
        IncreaseBetAmountInput(delta=delta, user_id=user.id)
    )
    return updated_bet


@router.get("", response_model=list[BetOut])
async def get_user_bets(
        bet_params: Annotated[
            BetParams, Query(title="Filters & sorting params")
        ],
        get_user_bets_use_case=Depends(get_get_user_bets_use_case),
        user: User = Depends(get_current_active_verified_user),
):
    bets = await get_user_bets_use_case.execute(
        GetUserBetsInput(params=bet_params, user_id=user.id)
    )
    return bets
