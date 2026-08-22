from decimal import Decimal, ROUND_HALF_UP

from app.database.models import Discount


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