from decimal import Decimal
from datetime import datetime, timezone
import logging

from app.repositories import (
    OrderRepository, OrderItemRepository, CartRepository, 
    ProductVariantRepository, DiscountRepository, PromoCodeRepository,
)
from app.database import (
    Order, OrderCreate,
    CartItem, ProductVariant, PromoCode,
    OrderStatus, PaymentStatus, OrderItem,
    CartStatus, OrderCancel, 
)
from app.exceptions import (
    ProductVariantNotFoundError, InsufficientStockError,
    PromoCodeNotFoundError, EmptyCartError,
    OrderNotFoundError, OrderCannotBeCancelledError
)
from app.core.pricing import (
    calculate_final_price, validate_promo_code_rules, calculate_promo_discount
)
from app.core.order_state_machine import (
    validate_order_status_transition, validate_payment_status_transition
)
from app.services.payments import PaymentService
from app.services.email import EmailService


logger = logging.getLogger(__name__)


class OrderService:

    def __init__(
            self,
            order_repo: OrderRepository,
            order_item_repo: OrderItemRepository,
            cart_repo: CartRepository,
            variant_repo: ProductVariantRepository,
            discount_repo: DiscountRepository,
            promo_code_repo: PromoCodeRepository,
            payment_service: PaymentService,
            email_service: EmailService,
    ):
        self.order_repo = order_repo
        self.order_item_repo = order_item_repo
        self.cart_repo = cart_repo
        self.variant_repo = variant_repo
        self.discount_repo = discount_repo
        self.promo_code_repo = promo_code_repo
        self.payment_service = payment_service
        self.email_service = email_service


    async def _lock_and_validate_stock(self, cart_items: list[CartItem]) -> dict[int, ProductVariant]:
        locked_variants = {}
        for item in cart_items:
            variant = await self.variant_repo.get_by_id_for_update(variant_id=item.variant_id)
            if variant is None:
                raise ProductVariantNotFoundError(variant_id=item.variant_id)
            if variant.stock_quantity < item.quantity:
                raise InsufficientStockError(
                    variant_id=item.variant_id, requested=item.quantity, available=variant.stock_quantity,
                )
            locked_variants[item.variant_id] = variant
        return locked_variants


    async def _calculate_item_price(self, variant: ProductVariant) -> Decimal:
        discounts = await self.discount_repo.get_active_for_variant(variant_id=variant.id)
        if not discounts:
            discounts = await self.discount_repo.get_active_for_category(category_id=variant.product.category_id)

        discount = discounts[0] if discounts else None

        return calculate_final_price(price=variant.price, discount=discount)


    async def _validate_and_apply_promo_code(
            self, subtotal: Decimal, code: str | None = None
    ) -> tuple[PromoCode | None, Decimal]:
        if not code:
            return (None, Decimal("0"))
        promo_code = await self.promo_code_repo.get_by_code(code=code)
        if promo_code is None:
            raise PromoCodeNotFoundError()
        validate_promo_code_rules(promo_code=promo_code, cart_total=subtotal)
        discount_amount = calculate_promo_discount(promo_code=promo_code, cart_total=subtotal)
        return (promo_code, discount_amount)


    async def create_order_from_cart(
            self, user_id: int, data: OrderCreate,
    ) -> tuple[Order, str]:
        from app.tasks.orders import cancel_unpaid_order

        active_cart = await self.cart_repo.get_active_cart(user_id=user_id)
        if active_cart is None or not active_cart.items:
            raise EmptyCartError()

        locked_variants: dict[int, ProductVariant] = await self._lock_and_validate_stock(cart_items=active_cart.items)
        order_item_data = []
        for item in active_cart.items:
            variant = locked_variants[item.variant_id]
            item_price = await self._calculate_item_price(variant=variant)
            order_item_data.append({
                "variant_id": item.variant_id,
                "quantity": item.quantity,
                "price": item_price,
            })

        subtotal = sum(
            (entry["price"] * entry["quantity"] for entry in order_item_data), Decimal("0")
        )
        promo_code, discount_amount = await self._validate_and_apply_promo_code(subtotal=subtotal, code=data.promo_code)
        total_amount = subtotal - discount_amount

        order = Order(
            user_id=user_id,
            status=OrderStatus.created,
            payment_status=PaymentStatus.pending,
            total_amount=total_amount,
            discount_amount=discount_amount,
            promo_code_id=promo_code.id if promo_code else None,
            shipping_address_id=data.shipping_address_id,
        )
        order = await self.order_repo.create(data=order)

        for entry in order_item_data:
            order_item = OrderItem(
                order_id=order.id,
                variant_id=entry["variant_id"],
                quantity=entry["quantity"],
                price=entry["price"],
            )
            await self.order_item_repo.create(data=order_item)

        for entry in order_item_data:
            variant = locked_variants[entry["variant_id"]]
            variant.stock_quantity -= entry["quantity"]
            await self.variant_repo.update(variant=variant)

        if promo_code is not None:
            promo_code.usage_count += 1
            await self.promo_code_repo.update(code=promo_code)

        await self.cart_repo.change_status(cart=active_cart, status=CartStatus.converted)

        final_order = await self.order_repo.get_by_id(order_id=order.id)
        session_id, checkout_url = await self.payment_service.create_payment_session(
            order_id=order.id, amount=total_amount,
        )
        final_order.stripe_session_id = session_id
        final_order = await self.order_repo.update(data=final_order)

        cancel_unpaid_order.apply_async(args=[final_order.id], countdown=900)

        return final_order, checkout_url


    async def get_order(self, order_id: int) -> Order:
        order = await self.order_repo.get_by_id(order_id=order_id)
        if order is None:
            raise OrderNotFoundError(order_id=order_id)
        return order


    async def get_my_order(self, user_id: int, order_id: int) -> Order:
        order = await self.order_repo.get_by_id(order_id=order_id)
        if order is None:
            raise OrderNotFoundError(order_id=order_id)
        if order.user_id != user_id:
            raise OrderNotFoundError(order_id=order_id)
        return order


    async def get_all_orders(
            self,
            user_id: int | None = None,
            status: OrderStatus | None = None,
            skip: int = 0,
            limit: int = 20,
    ) -> list[Order]:
        return await self.order_repo.get_all(
            user_id=user_id,
            status=status,
            skip=skip,
            limit=limit,
        )


    async def get_my_orders(
            self,
            user_id: int,
            status: OrderStatus | None = None,
            skip: int = 0,
            limit: int = 20,
    ) -> list[Order]:
        return await self.get_all_orders(
            user_id=user_id,
            status=status,
            skip=skip,
            limit=limit,
        )


    async def _restore_stock(self, order: Order) -> None:
        for order_item in order.items:
            variant = await self.variant_repo.get_by_id_for_update(variant_id=order_item.variant_id)
            variant.stock_quantity += order_item.quantity
            await self.variant_repo.update(variant=variant)


    async def change_order_status(
            self, order_id: int, new_status: OrderStatus,
    ) -> Order:
        order = await self.get_order(order_id=order_id)
        validate_order_status_transition(current=order.status, new=new_status)
        if new_status == OrderStatus.cancelled:
            await self._restore_stock(order)
            order.cancelled_at = datetime.now(timezone.utc)
        if new_status == OrderStatus.delivered:
            order.delivered_at = datetime.now(timezone.utc)
        order.status = new_status
        return await self.order_repo.update(data=order)


    async def cancel_order(
            self, user_id: int,
            order_id: int, data: OrderCancel,
    ) -> Order:
        order = await self.get_my_order(user_id=user_id, order_id=order_id)

        if order.status != OrderStatus.created:
            raise OrderCannotBeCancelledError(
                order_id=order_id, current_status=order.status,
            )
        validate_order_status_transition(
            order.status, OrderStatus.cancelled,
        )
        await self._restore_stock(order)

        order.status = OrderStatus.cancelled
        order.cancelled_at = datetime.now(timezone.utc)
        order.cancellation_reason = data.cancellation_reason

        return await self.order_repo.update(data=order)


    async def handle_payment_success(self, order_id: int) -> Order:
        order = await self.get_order(order_id=order_id)
        validate_payment_status_transition(
            current=order.payment_status, new=PaymentStatus.paid,
        )
        validate_order_status_transition(
            current=order.status, new=OrderStatus.processing,
        )

        order.payment_status = PaymentStatus.paid
        order.status = OrderStatus.processing
        await self.order_repo.update(data=order)

        user_email = order.user.email

        try:
            await self.email_service.send_order_confirmation(order=order, user_email=user_email)
        except Exception:
            logger.warning(f"Failed to send confirmation email for order {order.id}")

        return order