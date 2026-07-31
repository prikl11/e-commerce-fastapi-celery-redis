from typing import Annotated
from fastapi import Depends

from app.repositories import ProductVariantRepository
from app.services import ProductVariantService
from app.dependencies import SessionDep


def get_product_variant_repository(db: SessionDep) -> ProductVariantRepository:
    return ProductVariantRepository(db)


def get_product_variant_service(repo: Annotated[ProductVariantRepository, Depends(get_product_variant_repository)]) -> ProductVariantService:
    return ProductVariantService(repo)


ProductVariantServiceDep = Annotated[ProductVariantService, Depends(get_product_variant_service)]