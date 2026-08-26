from decimal import Decimal

from app.database import ProductVariant
from app.repositories import DiscountRepository
from app.core.pricing import calculate_final_price


async def resolve_final_prices(
        variants: list[ProductVariant], discount_repo: DiscountRepository
) -> dict[int, Decimal]:
    variant_ids = [v.id for v in variants]
    category_ids = [v.product.category_id for v in variants]

    variant_discount = await discount_repo.get_active_for_variants_bulk(variant_ids=variant_ids)
    category_discount = await discount_repo.get_active_for_categories_bulk(category_ids=category_ids)

    variant_discount_map = {d.variant_id: d for d in variant_discount}
    category_discount_map = {d.category_id: d for d in category_discount}

    result = {}
    for variant in variants:
        discount = variant_discount_map.get(variant.id) or category_discount_map.get(variant.product.category_id)
        result[variant.id] = calculate_final_price(variant.price, discount)
    return result