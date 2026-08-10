from fastapi import APIRouter, Depends
from typing import Annotated

from app.database import PromoCodeCreate, PromoCodeUpdate, PromoCodeResponse, User, UserRole
from app.dependencies import PromoCodeServiceDep, require_roles

router = APIRouter(prefix="/promo-codes", tags=["promo_codes"])

@router.get("/", response_model=list[PromoCodeResponse])
async def get_all_promo_codes(
    service: PromoCodeServiceDep,
    _: Annotated[User, Depends(require_roles(UserRole.admin, UserRole.manager))],
    skip: int = 0,
    limit: int = 20,
):
    return await service.get_all(skip=skip, limit=limit)

@router.get("/code/{code}", response_model=PromoCodeResponse)
async def get_promo_code_by_code(
    service: PromoCodeServiceDep,
    _: Annotated[User, Depends(require_roles(UserRole.admin, UserRole.manager))],
    code: str,
):
    return await service.get_by_code(code=code)

@router.get("/{code_id}", response_model=PromoCodeResponse)
async def get_promo_code(
    service: PromoCodeServiceDep,
    _: Annotated[User, Depends(require_roles(UserRole.admin, UserRole.manager))],
    code_id: int,
):
    return await service.get_by_id(code_id=code_id)

@router.post("/", response_model=PromoCodeResponse, status_code=201)
async def create_promo_code(
    service: PromoCodeServiceDep,
    _: Annotated[User, Depends(require_roles(UserRole.admin, UserRole.manager))],
    data: PromoCodeCreate,
):
    return await service.create_promo_code(data=data) 

@router.patch("/{code_id}", response_model=PromoCodeResponse)
async def update_promo_code(
    service: PromoCodeServiceDep,
    _: Annotated[User, Depends(require_roles(UserRole.admin, UserRole.manager))],
    code_id: int,
    data: PromoCodeUpdate,
):
    return await service.update_promo_code(code_id=code_id, data=data)

@router.delete("/{code_id}", status_code=204)
async def delete_promo_code(
    service: PromoCodeServiceDep,
    _: Annotated[User, Depends(require_roles(UserRole.admin, UserRole.manager))],
    code_id: int,
):
    await service.delete_promo_code(code_id=code_id)