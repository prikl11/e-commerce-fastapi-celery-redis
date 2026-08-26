from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime, timezone

from app.database.models import Discount, PromoCode
from app.exceptions import (
    PromoCodeExpiredError, PromoCodeUsageLimitExceededError, PromoCodeMinOrderAmountError,
)


def calculate_final_price(price: Decimal, discount: Discount | None) -> Decimal:
        if discount is None:
            return price.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        if discount.discount_type == "percent":
            final_price = price * (
                 Decimal("1") - discount.discount / Decimal("100")
            )
        else:
            final_price = price - discount.discount
        return final_price.quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )


def validate_promo_code_rules(promo_code: PromoCode, cart_total: Decimal) -> None:
    now = datetime.now(timezone.utc)
    if promo_code.starts_at is not None and now < promo_code.starts_at:
        raise PromoCodeExpiredError(code=promo_code.code)
    if promo_code.expires_at is not None and now > promo_code.expires_at:
        raise PromoCodeExpiredError(code=promo_code.code)
    if promo_code.usage_limit is not None and promo_code.usage_count >= promo_code.usage_limit:
        raise PromoCodeUsageLimitExceededError(code=promo_code.code)
    if promo_code.min_order_amount is not None and cart_total < promo_code.min_order_amount:
        raise PromoCodeMinOrderAmountError()


def calculate_promo_discount(promo_code: PromoCode, cart_total: Decimal) -> Decimal:
    if promo_code.discount_type == "percent":
        return cart_total * promo_code.discount / 100
    return min(promo_code.discount, cart_total)