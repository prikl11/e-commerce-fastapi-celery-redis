from fastapi import APIRouter, Depends
from typing import Annotated

from app.dependencies import require_roles, UserServiceDep, CurrentUserDep
from app.database import UserResponse, UserUpdate, User, UserRole, RoleUpdate

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=list[UserResponse])
async def get_all_users(
    service: UserServiceDep,
    _: Annotated[User, Depends(require_roles(UserRole.admin, UserRole.manager))],
    skip: int = 0,
    limit: int = 20,
):
    return await service.get_all_users(skip, limit)

@router.get("/role/{role}", response_model=list[UserResponse])
async def get_users_by_role(
    service: UserServiceDep,
    _: Annotated[User, Depends(require_roles(UserRole.manager, UserRole.admin))],
    role: UserRole,
    skip: int = 0,
    limit: int = 20,
):
    return await service.get_users_by_role(
        role=role,
        skip=skip,
        limit=limit,
    )

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: CurrentUserDep):
    return current_user

@router.get("/email/{email}", response_model=UserResponse)
async def get_user_by_email(
    service: UserServiceDep,
    email: str,
    _: Annotated[User, Depends(require_roles(UserRole.admin, UserRole.manager))]
):
    return await service.get_user_by_email(email=email)

@router.get("/phone/{phone}", response_model=UserResponse)
async def get_user_by_phone(
    service: UserServiceDep,
    phone: str,
    _: Annotated[User, Depends(require_roles(UserRole.admin, UserRole.manager))]
):
    return await service.get_user_by_phone(phone=phone)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    service: UserServiceDep, 
    user_id: int,
    _: Annotated[User, Depends(require_roles(UserRole.admin, UserRole.manager))]
    ):
    return await service.get_user(user_id=user_id)

@router.patch("/me", response_model=UserResponse)
async def update_me(
    service: UserServiceDep,
    current_user: CurrentUserDep,
    data: UserUpdate,
):
    return await service.update_user(user_id=current_user.id, data=data)

@router.patch("/{user_id}/role", response_model=UserResponse)
async def change_user_role(
    service: UserServiceDep,
    user_id: int,
    data: RoleUpdate,
    _: Annotated[User, Depends(require_roles(UserRole.admin))]
):
    return await service.change_user_role(user_id=user_id, role=data.role)

@router.delete("/{user_id}", status_code=204)
async def delete_user(
    service: UserServiceDep,
    user_id: int,
    _: Annotated[User, Depends(require_roles(UserRole.admin))]
):
    return await service.delete_user(user_id=user_id)