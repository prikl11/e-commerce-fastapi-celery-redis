from fastapi import APIRouter

from app.dependencies import ProductServiceDep
from app.database import ProductResponse, ProductCreate, ProductUpdate


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
async def search_products(service: ProductServiceDep, q: str):
    return await service.search_products(query=q)

@router.get("/slug/{slug}", response_model=ProductResponse)
async def get_product_by_slug(service: ProductServiceDep, slug: str):
    return await service.get_product_by_slug(slug=slug)

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(service: ProductServiceDep, product_id: int):
    return await service.get_product(product_id=product_id)

@router.post("/", response_model=ProductResponse, status_code=201)
async def create_product(data: ProductCreate, service: ProductServiceDep):
    return await service.create_product(data=data)

@router.patch("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    data: ProductUpdate,
    service: ProductServiceDep,
):
    return await service.update_product(product_id=product_id, data=data)

@router.delete("/{product_id}", status_code=204)
async def delete_product(product_id: int, service: ProductServiceDep):
    await service.delete_product(product_id=product_id)