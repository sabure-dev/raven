from typing import Annotated

from fastapi import APIRouter, Body, Depends
from starlette import status

from core.dependencies.orders.use_cases import get_create_order_use_case
from core.dependencies.users.security import get_current_active_verified_user

from db.models.users import User
from schemas.orders.orders import OrderOut, OrderCreate, OrderItemCreate
from schemas.orders.use_cases import CreateOrderInput

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


@router.post("", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
async def create_order(
        order_items: Annotated[
            list[OrderItemCreate], Body(title="Данные для создания пунктов заказа")
        ],
        create_order_use_case=Depends(get_create_order_use_case),
        user: User = Depends(get_current_active_verified_user),
):
    order = await create_order_use_case.execute(
        CreateOrderInput(items=order_items, user_id=user.id)
    )
    return order
