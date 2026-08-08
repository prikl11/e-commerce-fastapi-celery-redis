from app.repositories import ProductVariantRepository
from app.database import ProductVariant, ProductVariantCreate, ProductVariantUpdate
from app.exceptions import ProductVariantNotFoundError, InsufficientStockError


class ProductVariantService:

    def __init__(self, repo: ProductVariantRepository):
        self.repo = repo


    async def get_variant(self, variant_id: int) -> ProductVariant:
        variant = await self.repo.get_by_id(variant_id=variant_id)
        if variant is None:
            raise ProductVariantNotFoundError(variant_id)
        return variant


    async def get_variant_by_product(self, product_id: int) -> list[ProductVariant]:
        return await self.repo.get_all_by_product(product_id=product_id)


    async def create_variant(
            self,
            product_id: int,
            data: ProductVariantCreate,
    ) -> ProductVariant:
        variant = ProductVariant(product_id=product_id, **data.model_dump(exclude={"product_id"}))
        return await self.repo.create(variant=variant)


    async def update_variant(
            self,
            variant_id: int,
            data: ProductVariantUpdate,
    ) -> ProductVariant:
        variant = await self.get_variant(variant_id=variant_id)
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(variant, key, value)
        return await self.repo.update(variant=variant)


    async def delete_variant(self, variant_id: int) -> None:
        variant = await self.get_variant(variant_id=variant_id)
        await self.repo.delete(variant=variant)


    async def adjust_stock(
            self,
            variant_id: int,
            delta: int,
    ) -> ProductVariant:
        variant = await self.repo.get_by_id_for_update(variant_id=variant_id)
        if variant_id is None:
            raise ProductVariantNotFoundError(variant_id)

        new_quantity = variant.stock_quantity + delta
        if new_quantity < 0:
            raise InsufficientStockError(
                variant_id=variant_id,
                requested=abs(delta),
                available=variant.stock_quantity,
            )

        variant.stock_quantity = new_quantity
        return await self.repo.update(variant=variant)