from fastapi import APIRouter, Depends
from typing import Annotated

from app.dependencies import AddressServiceDep, CurrentUserDep, require_roles
from app.database import (
    AddressUpdate, AddressCreate, AddressResponse, User, UserRole, AddressCreateRequest
)

router = APIRouter(prefix="/addresses", tags=["addresses"])

@router.get("/", response_model=list[AddressResponse])
async def get_all_addressess_by_user(
    service: AddressServiceDep,
    _: Annotated[User, Depends(require_roles(UserRole.admin, UserRole.manager))],
    user_id: int,
):
    return await service.get_all_by_user(user_id=user_id)

@router.get("/me", response_model=list[AddressResponse])
async def get_all_my_addresses(
    service: AddressServiceDep,
    current_user: CurrentUserDep,
):
    return await service.get_all_by_user(user_id=current_user.id)

@router.get("/me/{address_id}", response_model=AddressResponse)
async def get_my_address(
    service: AddressServiceDep,
    current_user: CurrentUserDep,
    address_id: int,
):
    return await service.get_by_id_and_user(address_id=address_id, user_id=current_user.id)

@router.get("/{address_id}", response_model=AddressResponse)
async def get_address(
    service: AddressServiceDep,
    _: Annotated[User, Depends(require_roles(UserRole.admin, UserRole.manager))],
    address_id: int,
):
    return await service.get_by_id(address_id=address_id)

@router.post("/", response_model=AddressResponse, status_code=201)
async def create_address(
    service: AddressServiceDep,
    data: AddressCreateRequest,
    current_user: CurrentUserDep,
):
    address = AddressCreate(**data.model_dump(), user_id=current_user.id)
    return await service.create(data=address)

@router.patch("/{address_id}", response_model=AddressResponse)
async def update_address(
    service: AddressServiceDep,
    address_id: int,
    data: AddressUpdate,
    current_user: CurrentUserDep,
):
    return await service.update(
        address_id=address_id,
        data=data,
        user_id=current_user.id
    )

@router.delete("/{address_id}", status_code=204) 
async def delete_address(
    service: AddressServiceDep,
    address_id: int,
    current_user: CurrentUserDep,
):
    await service.delete(
        address_id=address_id, user_id=current_user.id
    )