from fastapi import Depends
from typing import Annotated

from app.services import PaymentService


def get_payment_service() -> PaymentService:
    return PaymentService()

PaymentServiceDep = Annotated[PaymentService, Depends(get_payment_service)]