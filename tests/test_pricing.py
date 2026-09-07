import pytest
from decimal import Decimal
from datetime import datetime, timezone, timedelta

from app.core.pricing import calculate_final_price, calculate_promo_discount, validate_promo_code_rules
from app.database import Discount, DiscountType, PromoCode
from app.exceptions import PromoCodeMinOrderAmountError, PromoCodeExpiredError, PromoCodeUsageLimitExceededError


async def test_calculate_final_price_no_discount():
    assert calculate_final_price(price=Decimal("100.00"), discount=None) == Decimal("100.00")


async def test_calculate_final_price_percent_discount():
    assert calculate_final_price(
        price=Decimal("100.00"), discount=Discount(
            discount=Decimal("30"),
            discount_type=DiscountType.percent
        )
    ) == Decimal("70.00")


async def test_calculate_final_price_fixed_discount():
    discount = Discount(discount=Decimal("30"), discount_type=DiscountType.fixed)
    result = calculate_final_price(price=Decimal("100.00"), discount=discount)
    assert result == Decimal("70.00")


async def test_calculate_final_price_fixed_discount_larger_than_price():
    discount = Discount(discount=Decimal("130.00"), discount_type=DiscountType.fixed)
    result = calculate_final_price(price=Decimal("100.00"), discount=discount)
    assert result == Decimal("0")


async def test_calculate_promo_discount_percent():
    promo_code = PromoCode(code="test", discount=Decimal("30"), discount_type=DiscountType.percent)
    result = calculate_promo_discount(promo_code=promo_code, cart_total=Decimal("1400.00"))
    assert result == Decimal("420.00")


async def test_calculate_promo_discount_fixed_larger_than_total():
    promo_code = PromoCode(code="test", discount=Decimal("1500.00"), discount_type=DiscountType.fixed)
    result = calculate_promo_discount(promo_code=promo_code, cart_total=Decimal("1200.00"))
    assert result == Decimal("1200.00")


async def test_validate_promo_code_rules_expired():
    with pytest.raises(PromoCodeExpiredError):
        promo_code = PromoCode(
            code="test", 
            discount=Decimal("30"), 
            discount_type=DiscountType.percent,
            expires_at=datetime.now(timezone.utc) - timedelta(days=2)
        )
        validate_promo_code_rules(promo_code=promo_code, cart_total=Decimal("100.00"))


async def test_validate_promo_code_rules_not_started_yet():
    with pytest.raises(PromoCodeExpiredError):
        promo_code = PromoCode(
            code="test", 
            discount=Decimal("30"), 
            discount_type=DiscountType.percent,
            starts_at=datetime.now(timezone.utc) + timedelta(days=2)
        )
        validate_promo_code_rules(promo_code=promo_code, cart_total=Decimal("100"))


async def test_validate_promo_code_rules_usage_limit_exceeded():
    with pytest.raises(PromoCodeUsageLimitExceededError):
        promo_code = PromoCode(
            code="test", 
            discount=Decimal("30"), 
            discount_type=DiscountType.percent,
            usage_limit=3,
            usage_count=4,
        )
        validate_promo_code_rules(promo_code=promo_code, cart_total=Decimal("100"))


async def test_validate_promo_rules_below_min_order_amount():
    with pytest.raises(PromoCodeMinOrderAmountError):
        promo_code = PromoCode(
            code="test", 
            discount=Decimal("30"), 
            discount_type=DiscountType.percent,
            min_order_amount=Decimal("100"),
        )
        validate_promo_code_rules(promo_code=promo_code, cart_total=Decimal("20"))


async def test_validate_promo_code_rules_valid():
        promo_code = PromoCode(
            code="test", 
            discount=Decimal("30"), 
            discount_type=DiscountType.percent,
        )
        validate_promo_code_rules(promo_code=promo_code, cart_total=Decimal("100"))