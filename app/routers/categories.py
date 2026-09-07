from fastapi import APIRouter, Depends
from typing import Annotated

from app.dependencies import CategoryServiceDep, require_roles
from app.database import CategoryResponse, CategoryCreate, CategoryUpdate, User, UserRole


router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/", response_model=list[CategoryResponse])
async def get_all_categories(
    service: CategoryServiceDep, 
    _: Annotated[User, Depends(require_roles(UserRole.admin, UserRole.manager))],
    parent_id: int | None = None
):
    return await service.get_all_categories(parent_id=parent_id)

@router.get("/slug/{slug}", response_model=CategoryResponse)
async def get_category_by_slug(
    service: CategoryServiceDep, 
    _: Annotated[User, Depends(require_roles(UserRole.admin, UserRole.manager))],
    slug: str,
):
    return await service.get_category_by_slug(slug=slug)

@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(
    service: CategoryServiceDep, 
    _: Annotated[User, Depends(require_roles(UserRole.admin, UserRole.manager))],
    category_id: int,
):
    return await service.get_category(category_id=category_id)

@router.post("/", response_model=CategoryResponse, status_code=201)
async def create_category(
    data: CategoryCreate, 
    service: CategoryServiceDep,
    _: Annotated[User, Depends(require_roles(UserRole.admin, UserRole.manager))],
):
    return await service.create_category(data=data)

@router.patch("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int, 
    data: CategoryUpdate, 
    service: CategoryServiceDep,
    _: Annotated[User, Depends(require_roles(UserRole.admin, UserRole.manager))],
    ):
    return await service.update_category(category_id=category_id, data=data)

@router.delete("/{category_id}", status_code=204)
async def delete_category(
    category_id: int, 
    service: CategoryServiceDep,
    _: Annotated[User, Depends(require_roles(UserRole.admin, UserRole.manager))],
    ):
    await service.delete_category(category_id=category_id)