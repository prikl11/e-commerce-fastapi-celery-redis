from typing import Annotated
from fastapi import Depends

from app.repositories import ProductRepository
from app.services import ProductService
from app.dependencies import SessionDep


def get_product_repository(db: SessionDep) -> ProductRepository:
    return ProductRepository(db)


def get_product_service(repo: Annotated[ProductRepository, Depends(get_product_repository)]) -> ProductService:
    return ProductService(repo)


ProductServiceDep = Annotated[ProductService, Depends(get_product_service)]