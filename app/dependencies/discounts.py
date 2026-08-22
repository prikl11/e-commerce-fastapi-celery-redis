from typing import Annotated
from fastapi import Depends

from app.repositories import DiscountRepository
from app.services import DiscountService
from app.dependencies import SessionDep


def get_discount_repository(db: SessionDep) -> DiscountRepository:
    return DiscountRepository(db)

DiscountRepositoryDep = Annotated[DiscountRepository, Depends(get_discount_repository)]

def get_discount_service(repo: DiscountRepositoryDep) -> DiscountService:
    return DiscountService(repo)

DiscountServiceDep = Annotated[DiscountService, Depends(get_discount_service)]