from fastapi import APIRouter, Depends
from typing import Annotated

from app.dependencies import CartServiceDep, require_roles, CurrentUserDep
from app.database import CartResponse, CartItemCreate, CartItemUpdate, User, UserRole, CartStatus

router = APIRouter(prefix="/carts", tags=["carts"])

@router.get("/", response_model=list[CartResponse])
async def get_all_carts(
    service: CartServiceDep,
    _: Annotated[User, Depends(require_roles(UserRole.admin, UserRole.manager))],
    skip: int = 0,
    limit: int = 20,
):
    return await service.get_all_response(skip=skip, limit=limit)

@router.get("/user/me", response_model=list[CartResponse])
async def get_all_my_carts(
    service: CartServiceDep,
    current_user: CurrentUserDep,
    skip: int = 0,
    limit: int = 20,
):
    return await service.get_all_response_by_user(
        user_id=current_user.id,
        skip=skip,
        limit=limit
    )

@router.get("/user/{user_id}", response_model=list[CartResponse])
async def get_all_carts_by_user(
    service: CartServiceDep,
    user_id: int,
    _: Annotated[User, Depends(require_roles(UserRole.admin, UserRole.manager))],
    skip: int = 0,
    limit: int = 20,
):
    return await service.get_all_response_by_user(
        user_id=user_id,
        skip=skip,
        limit=limit,
    )

@router.get("/status/{status}", response_model=list[CartResponse])
async def get_all_carts_by_status(
    service: CartServiceDep,
    _: Annotated[User, Depends(require_roles(UserRole.admin, UserRole.manager))],
    status: CartStatus = CartStatus.active,
    skip: int = 0,
    limit: int = 20,
):
    return await service.get_all_response_by_status(
        status=status,
        skip=skip,
        limit=limit
    )

@router.get("/me/status/{status}", response_model=list[CartResponse])
async def get_all_my_carts_by_status(
    service: CartServiceDep,
    current_user: CurrentUserDep,
    status: CartStatus = CartStatus.active,
    skip: int = 0,
    limit: int = 20,
):
    return await service.get_all_response_by_user_and_status(
        user_id=current_user.id,
        status=status,
        skip=skip,
        limit=limit,
    )

@router.get("/user-status/{user_id}/{status}", response_model=list[CartResponse])
async def get_all_carts_by_user_and_status(
    service: CartServiceDep,
    user_id: int,
    _: Annotated[User, Depends(require_roles(UserRole.admin, UserRole.manager))],
    status: CartStatus = CartStatus.active,
    skip: int = 0,
    limit: int = 20,
):
    return await service.get_all_response_by_user_and_status(
        user_id=user_id,
        status=status,
        skip=skip,
        limit=limit
    )

@router.get("/me", response_model=CartResponse)
async def get_my_active_cart(
    service: CartServiceDep,
    current_user: CurrentUserDep,
):
    return await service.get_my_cart_response(user_id=current_user.id)

@router.get("/me/{cart_id}", response_model=CartResponse)
async def get_my_cart_by_id(
    service: CartServiceDep,
    current_user: CurrentUserDep,
    cart_id: int,
):
    return await service.get_my_cart_response_by_id(user_id=current_user.id, cart_id=cart_id)

@router.get("/{cart_id}", response_model=CartResponse)
async def get_cart_by_id(
    service: CartServiceDep,
    _: Annotated[User, Depends(require_roles(UserRole.admin, UserRole.manager))],
    cart_id: int,
):
    return await service.get_cart_response_by_id(cart_id=cart_id)

@router.post("/items", response_model=CartResponse, status_code=201)
async def add_item(
    service: CartServiceDep,
    data: CartItemCreate,
    current_user: CurrentUserDep,
):
    return await service.add_item(user_id=current_user.id, data=data)

@router.patch("/items/{variant_id}", response_model=CartResponse)
async def change_quantity(
    service: CartServiceDep,
    variant_id: int,
    data: CartItemUpdate,
    current_user: CurrentUserDep,
):
    return await service.update_item_quantity(
        user_id=current_user.id,
        variant_id=variant_id,
        new_quantity=data.quantity,
    )

@router.delete("/items/{variant_id}", response_model=CartResponse)
async def remove_item(
    service: CartServiceDep,
    current_user: CurrentUserDep,
    variant_id: int,
):
    return await service.remove_item(user_id=current_user.id, variant_id=variant_id)