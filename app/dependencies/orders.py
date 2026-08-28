from fastapi import Depends
from typing import Annotated

from app.dependencies import SessionDep
from app.dependencies.carts import get_cart_repository
from app.dependencies.product_variants import get_product_variant_repository
from app.dependencies.discounts import get_discount_repository
from app.dependencies.promo_codes import get_promo_code_repository
from app.dependencies.payments import get_payment_service
from app.dependencies.email import get_email_service
from app.repositories import (
    OrderRepository, OrderItemRepository,
    PromoCodeRepository, ProductVariantRepository,
    DiscountRepository, CartRepository
)
from app.services import OrderService, PaymentService, EmailService


def get_order_repository(db: SessionDep) -> OrderRepository:
    return OrderRepository(db)

def get_order_item_repository(db: SessionDep) -> OrderItemRepository:
    return OrderItemRepository(db)

OrderRepoDep = Annotated[OrderRepository, Depends(get_order_repository)]
OrderItemRepoDep = Annotated[OrderItemRepository, Depends(get_order_item_repository)]
CartRepoDep = Annotated[CartRepository, Depends(get_cart_repository)]
ProductVariantRepoDep = Annotated[ProductVariantRepository, Depends(get_product_variant_repository)]
DiscountRepoDep = Annotated[DiscountRepository, Depends(get_discount_repository)]
PromoCodeRepoDep = Annotated[PromoCodeRepository, Depends(get_promo_code_repository)]
PaymentServiceDep = Annotated[PaymentService, Depends(get_payment_service)]
EmailServiceDep = Annotated[EmailService, Depends(get_email_service)]

def get_order_service(
        order_repo: OrderRepoDep,
        order_item_repo: OrderItemRepoDep,
        cart_repo: CartRepoDep,
        variant_repo: ProductVariantRepoDep,
        discount_repo: DiscountRepoDep,
        promo_code_repo: PromoCodeRepoDep,
        payment_service: PaymentServiceDep,
        email_service: EmailServiceDep,
) -> OrderService:
    return OrderService(
        order_repo=order_repo,
        order_item_repo=order_item_repo,
        cart_repo=cart_repo,
        variant_repo=variant_repo,
        discount_repo=discount_repo,
        promo_code_repo=promo_code_repo,
        payment_service=payment_service,
        email_service=email_service,
    )

OrderServiceDep = Annotated[OrderService, Depends(get_order_service)]