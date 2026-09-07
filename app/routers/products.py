from fastapi import APIRouter, Depends
from typing import Annotated

from app.dependencies import ProductServiceDep, require_roles
from app.database import ProductResponse, ProductCreate, ProductUpdate, User, UserRole


router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=list[ProductResponse])
async def get_all_products(
    service: ProductServiceDep,
    category_id: int | None = None,
    skip: int = 0,
    limit: int = 20,
):
    return await service.get_all_products(
        category_id=category_id,
        skip=skip,
        limit=limit
    )

@router.get("/search", response_model=list[ProductResponse])
async def search_products(
    service: ProductServiceDep, 
    q: str,
    _: Annotated[User, Depends(require_roles(UserRole.admin, UserRole.manager))],
):
    return await service.search_products(query=q)

@router.get("/slug/{slug}", response_model=ProductResponse)
async def get_product_by_slug(
    service: ProductServiceDep, 
    slug: str,
    _: Annotated[User, Depends(require_roles(UserRole.admin, UserRole.manager))],
):
    return await service.get_product_by_slug(slug=slug)

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    service: ProductServiceDep, 
    product_id: int,
    _: Annotated[User, Depends(require_roles(UserRole.admin, UserRole.manager))],
):
    return await service.get_product(product_id=product_id)

@router.post("/", response_model=ProductResponse, status_code=201)
async def create_product(
    data: ProductCreate, 
    service: ProductServiceDep,
    _: Annotated[User, Depends(require_roles(UserRole.admin, UserRole.manager))],
):
    return await service.create_product(data=data)

@router.patch("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    data: ProductUpdate,
    service: ProductServiceDep,
    _: Annotated[User, Depends(require_roles(UserRole.admin, UserRole.manager))],
):
    return await service.update_product(product_id=product_id, data=data)

@router.delete("/{product_id}", status_code=204)
async def delete_product(
    product_id: int, 
    service: ProductServiceDep,
    _: Annotated[User, Depends(require_roles(UserRole.admin, UserRole.manager))],
):
    await service.delete_product(product_id=product_id)