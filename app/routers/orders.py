from fastapi import APIRouter, Depends
from typing import Annotated

from app.dependencies import (
    CurrentUserDep, require_roles,
    OrderServiceDep
)
from app.database import (
    User, UserRole, OrderCreate,
    OrderResponse, OrderStatus,
    OrderCancel, OrderStatusUpdate,
    OrderCreateResponse
)

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=OrderCreateResponse, status_code=201)
async def create_order_from_cart(
    service: OrderServiceDep,
    current_user: CurrentUserDep,
    data: OrderCreate,
):
    order, payment_url = await service.create_order_from_cart(
        user_id=current_user.id, data=data,
    )
    return OrderCreateResponse(order=order, payment_url=payment_url)

@router.get("/me", response_model=list[OrderResponse])
async def get_my_orders(
    service: OrderServiceDep,
    current_user: CurrentUserDep,
    status: OrderStatus | None = None,
    skip: int = 0,
    limit: int = 20,
):
    return await service.get_my_orders(
        user_id=current_user.id, status=status,
        skip=skip, limit=limit
    )

@router.get("/me/{order_id}", response_model=OrderResponse)
async def get_my_order(
    service: OrderServiceDep,
    current_user: CurrentUserDep,
    order_id: int,
):
    return await service.get_my_order(user_id=current_user.id, order_id=order_id)

@router.post("/me/{order_id}/cancel", response_model=OrderResponse)
async def cancel_my_order(
    service: OrderServiceDep,
    current_user: CurrentUserDep,
    order_id: int,
    data: OrderCancel,
):
    return await service.cancel_order(
        user_id=current_user.id, order_id=order_id, data=data,
    )

@router.get("/", response_model=list[OrderResponse])
async def get_all_orders(
    service: OrderServiceDep,
    _: Annotated[User, Depends(require_roles(UserRole.admin, UserRole.manager))],
    status: OrderStatus | None = None,
    skip: int = 0,
    limit: int = 20,
):
    return await service.get_all_orders(
        status=status, skip=skip, limit=limit,
    )

@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    service: OrderServiceDep,
    _: Annotated[User, Depends(require_roles(UserRole.admin, UserRole.manager))],
    order_id: int,
):
    return await service.get_order(order_id=order_id)

@router.patch("/{order_id}/status", response_model=OrderResponse)
async def change_status(
    service: OrderServiceDep,
    _: Annotated[User, Depends(require_roles(UserRole.admin, UserRole.manager))],
    order_id: int,
    data: OrderStatusUpdate,
):
    return await service.change_order_status(
        order_id=order_id, new_status=data.status,
    )