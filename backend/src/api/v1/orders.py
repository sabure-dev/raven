from typing import Annotated

from fastapi import APIRouter, Body, Depends, Query, Path
from starlette import status

from core.dependencies.orders.use_cases import get_create_order_use_case, get_get_orders_use_case, \
    get_cancel_order_use_case
from core.dependencies.users.security import get_current_active_verified_user

from db.models.users import User
from schemas.orders.orders import OrderOut, OrderItemCreate, OrderParams
from schemas.orders.use_cases import CreateOrderInput, GetOrdersInput, CancelOrderInput

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


@router.get("", response_model=list[OrderOut], status_code=status.HTTP_200_OK)
async def get_user_orders(
        order_params: Annotated[
            OrderParams, Query(title="Параметры для фильтрации и сортировки")
        ],
        get_orders_use_case=Depends(get_get_orders_use_case),
        user: User = Depends(get_current_active_verified_user),
):
    orders = await get_orders_use_case.execute(
        GetOrdersInput(user_id=user.id, params=order_params)
    )
    return orders


@router.patch("/{order_id}", response_model=OrderOut, status_code=status.HTTP_200_OK)
async def cancel_order(
        order_id: Annotated[int, Path(title="ID of order to cancel")],
        cancel_order_use_case=Depends(get_cancel_order_use_case),
        user: User = Depends(get_current_active_verified_user),
):
    order = await cancel_order_use_case.execute(
        CancelOrderInput(order_id=order_id, user_id=user.id)
    )
    return order
