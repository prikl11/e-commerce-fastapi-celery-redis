import asyncio
from datetime import datetime, timezone

from app.core.celery_app import celery_app
from app.database.db import AsyncSessionLocal
from app.database.enums import OrderStatus, PaymentStatus
from app.services import (
    OrderService, PaymentService, EmailService
)
from app.repositories import (
    OrderRepository, OrderItemRepository,
    CartRepository, ProductVariantRepository,
    DiscountRepository, PromoCodeRepository
)
from app.core.order_state_machine import (
    validate_order_status_transition,
    validate_payment_status_transition,
)

@celery_app.task
def cancel_unpaid_order(order_id: int) -> None:
    asyncio.run(_cancel_unpaid_order_async(order_id))


async def _cancel_unpaid_order_async(order_id: int) -> None:
    async with AsyncSessionLocal() as session:
        order_repo = OrderRepository(session)
        order_item_repo = OrderItemRepository(session)
        cart_repo = CartRepository(session)
        variant_repo = ProductVariantRepository(session)
        discount_repo = DiscountRepository(session)
        promo_code_repo = PromoCodeRepository(session)
        payment_service = PaymentService()
        email_service = EmailService()

        order_service = OrderService(
            order_repo=order_repo,
            order_item_repo=order_item_repo,
            cart_repo=cart_repo,
            variant_repo=variant_repo,
            discount_repo=discount_repo,
            promo_code_repo=promo_code_repo,
            payment_service=payment_service,
            email_service=email_service,
        )

        order = await order_service.get_order(order_id=order_id)

        if order.status == OrderStatus.paid:
            return

        validate_order_status_transition(
            current=order.status, new=OrderStatus.cancelled
        )
        validate_payment_status_transition(
            current=order.payment_status, new=PaymentStatus.failed,
        )

        await order_service._restore_stock(order)
        order.status = OrderStatus.cancelled
        order.cancelled_at = datetime.now(timezone.utc)
        order.payment_status = PaymentStatus.failed
        
        await order_service.order_repo.update(data=order)
        await session.commit()