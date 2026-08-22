from typing import Annotated
from fastapi import Depends

from app.repositories import ProductRepository
from app.services import ProductService
from app.dependencies import SessionDep
from app.dependencies.discounts import DiscountRepositoryDep


def get_product_repository(db: SessionDep) -> ProductRepository:
    return ProductRepository(db)


def get_product_service(
        repo: Annotated[ProductRepository, Depends(get_product_repository)], discount_repo: DiscountRepositoryDep
        ) -> ProductService:
    return ProductService(repo, discount_repo)


ProductServiceDep = Annotated[ProductService, Depends(get_product_service)]