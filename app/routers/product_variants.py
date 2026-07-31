from fastapi import APIRouter

from app.dependencies import ProductVariantServiceDep
from app.database import (
    ProductVariantAdminResponse, ProductVariantCreate, ProductVariantUpdate, StockAdjustment,
)

router = APIRouter(prefix="/products/{product_id}/variants", tags=["product_variants"])


@router.get("/", response_model=list[ProductVariantAdminResponse])
async def get_variants(product_id: int, service: ProductVariantServiceDep):
    return await service.get_variant_by_product(product_id=product_id)

@router.get("/{variant_id}", response_model=ProductVariantAdminResponse)
async def get_variant(
    product_id: int,
    variant_id: int,
    service: ProductVariantServiceDep,
):
    return await service.get_variant(variant_id=variant_id)

@router.post("/", response_model=ProductVariantAdminResponse, status_code=201)
async def create_variant(
    product_id: int,
    data: ProductVariantCreate,
    service: ProductVariantServiceDep,
):
    return await service.create_variant(product_id=product_id, data=data)

@router.patch("/{variant_id}", response_model=ProductVariantAdminResponse)
async def update_variant(
    product_id: int,
    variant_id: int,
    data: ProductVariantUpdate,
    service: ProductVariantServiceDep,
):
    return await service.update_variant(variant_id=variant_id, data=data)

@router.delete("/{variant_id}", status_code=204)
async def delete_variant(
    product_id: int,
    variant_id: int,
    service: ProductVariantServiceDep,
):
    await service.delete_variant(variant_id=variant_id)

@router.post("/{variant_id}/stock", response_model=ProductVariantAdminResponse)
async def adjust_stock(
    product_id: int,
    variant_id: int,
    data: StockAdjustment,
    service: ProductVariantServiceDep,
):
    return await service.adjust_stock(variant_id=variant_id, delta=data.delta)