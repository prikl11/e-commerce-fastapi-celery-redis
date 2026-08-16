from fastapi import APIRouter, Depends
from typing import Annotated

from app.database import DiscountCreate, DiscountUpdate, User, DiscountResponse, UserRole
from app.dependencies import require_roles, DiscountServiceDep

router = APIRouter(prefix="/discounts", tags=["discounts"])

@router.get("/", response_model=list[DiscountResponse])
async def get_all_discounts(
    service: DiscountServiceDep,
    _: Annotated[User, Depends(require_roles(UserRole.admin, UserRole.manager))],
    skip: int = 0,
    limit: int = 20,
):
    return await service.get_all(skip=skip, limit=limit)

@router.get("/active/variant/{variant_id}", response_model=list[DiscountResponse])
async def get_active_discounts_for_variant(
    service: DiscountServiceDep,
    _: Annotated[User, Depends(require_roles(UserRole.admin, UserRole.manager))],
    variant_id: int,
):
    return await service.get_active_for_variant(variant_id=variant_id)

@router.get("/active/category/{category_id}", response_model=list[DiscountResponse])
async def get_active_discounts_for_category(
    service: DiscountServiceDep,
    _: Annotated[User, Depends(require_roles(UserRole.admin, UserRole.manager))],
    category_id: int,
):
    return await service.get_active_for_category(category_id=category_id)

@router.post("/", response_model=DiscountResponse, status_code=201)
async def create_discount(
    service: DiscountServiceDep,
    _: Annotated[User, Depends(require_roles(UserRole.admin, UserRole.manager))],
    data: DiscountCreate,
):
    return await service.create(data=data)

@router.patch("/{discount_id}", response_model=DiscountResponse)
async def update_discount(
    service: DiscountServiceDep,
    _: Annotated[User, Depends(require_roles(UserRole.admin, UserRole.manager))],
    discount_id: int,
    data: DiscountUpdate,
):
    return await service.update(discount_id=discount_id, data=data)

@router.delete("/{discount_id}", status_code=204)
async def delete_discount(
    service: DiscountServiceDep,
    _: Annotated[User, Depends(require_roles(UserRole.admin, UserRole.manager))],
    discount_id: int,
):
    await service.delete(discount_id=discount_id)