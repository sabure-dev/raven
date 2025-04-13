from fastapi import APIRouter, Depends

from core.dependencies.rounds.use_case import get_create_round_use_case, get_get_current_round_use_case
from core.dependencies.users.security import get_current_superuser
from db.models import User
from schemas.rounds.rounds import RoundOut, RoundCreate
from schemas.rounds.use_cases import CreateRoundInput

router = APIRouter(prefix="/rounds",
                   tags=["Rounds"])


@router.post("", response_model=RoundOut)
async def create_round(
        round_to_create: RoundCreate,
        create_round_use_case=Depends(get_create_round_use_case),
        _: User = Depends(get_current_superuser),
):
    created_round = await create_round_use_case.execute(
        CreateRoundInput(round=round_to_create)
    )
    return created_round


@router.get("/current", response_model=RoundOut)
async def get_current_round(
        get_current_round_use_case=Depends(get_get_current_round_use_case),
):
    current_round = await get_current_round_use_case.execute()
    return current_round
