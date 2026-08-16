from decimal import Decimal

from app.database import Discount


def calculate_final_price(price: Decimal, discount: Discount | None) -> Decimal:
        if discount is None:
            return price
        if discount.discount_type == "percent":
            return price - (price * discount.discount / 100)
        return max(price - discount.discount, Decimal("0"))