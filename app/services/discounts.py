from app.repositories import DiscountRepository
from app.database import Discount, DiscountCreate, DiscountUpdate, ProductVariant
from app.exceptions import DiscountNotFoundError, DiscountAlreadyExistsError
from app.core.pricing import calculate_final_price


class DiscountService:

    def __init__(self, repo: DiscountRepository):
        self.repo = repo


    async def get_all(self, skip: int = 0, limit: int = 20) -> list[Discount]:
        return await self.repo.get_all(skip=skip, limit=limit)


    async def get_by_id(self, discount_id: int) -> Discount:
        discount = await self.repo.get_by_id(discount_id=discount_id)
        if discount is None:
            raise DiscountNotFoundError()
        return discount


    async def get_active_for_variant(self, variant_id: int) -> list[Discount]:
        return await self.repo.get_active_for_variant(variant_id=variant_id)


    async def get_active_for_category(self, category_id: int) -> list[Discount]:
        return await self.repo.get_active_for_category(category_id=category_id)


    async def get_active_for_variants_bulk(self, variant_ids: list[int]) -> list[Discount]:
        return await self.repo.get_active_for_variants_bulk(variant_ids=variant_ids)


    async def get_active_for_categories_bulk(self, category_ids: list[int]) -> list[Discount]:
        return await self.repo.get_active_for_categories_bulk(category_ids=category_ids)


    async def get_applicable_discount(self, variant: ProductVariant) -> Discount | None:
        variant_discounts = await self.get_active_for_variant(variant_id=variant.id)
        if variant_discounts:
            return variant_discounts[0]

        category_discounts = await self.get_active_for_category(category_id=variant.product.category_id)
        if category_discounts:
            return category_discounts[0]

        return None


    async def create(self, data: DiscountCreate) -> Discount:
        discount = Discount(**data.model_dump())
        return await self.repo.create(data=discount)


    async def update(self, discount_id: int, data: DiscountUpdate) -> Discount:
        discount = await self.get_by_id(discount_id=discount_id)

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(discount, key, value)

        return await self.repo.update(data=discount)


    async def delete(self, discount_id: int) -> None:
        discount = await self.get_by_id(discount_id=discount_id)
        await self.repo.delete(data=discount)