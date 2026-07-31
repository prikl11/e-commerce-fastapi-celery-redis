from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import ProductVariant


class ProductVariantRepository:

    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_by_id(self, variant_id: int) -> ProductVariant | None:
        return await self.session.get(ProductVariant, variant_id)


    async def get_by_id_for_update(self, variant_id: int) -> ProductVariant | None:
        stmt = select(ProductVariant).where(ProductVariant.id == variant_id).with_for_update()
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


    async def get_all_by_product(self, product_id: int) -> list[ProductVariant]:
        stmt = select(ProductVariant).where(ProductVariant.product_id == product_id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())


    async def create(self, variant: ProductVariant) -> ProductVariant:
        self.session.add(variant)
        await self.session.flush()
        return variant


    async def update(self, variant: ProductVariant) -> ProductVariant:
        await self.session.flush()
        stmt = (
            select(ProductVariant)
            .where(ProductVariant.id == variant.id)
            .execution_options(populate_existing=True)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one()


    async def delete(self, variant: ProductVariant) -> None:
        await self.session.delete(variant)
        await self.session.flush()