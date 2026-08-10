from typing import Annotated
from fastapi import Depends

from app.repositories import PromoCodeRepository
from app.services import PromoCodeService
from app.dependencies import SessionDep


def get_promo_code_repository(db: SessionDep) -> PromoCodeRepository:
    return PromoCodeRepository(db)

def get_promo_code_service(repo: Annotated[PromoCodeRepository, Depends(get_promo_code_repository)]):
    return PromoCodeService(repo)

PromoCodeServiceDep = Annotated[PromoCodeService, Depends(get_promo_code_service)]