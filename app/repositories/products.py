from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import Product


class ProductRepository:

    def __init__(self, session: AsyncSession):
        self.session = session


    async def search(self, query: str) -> list[Product]:
        ts_query = func.plainto_tsquery("russian", query)
        stmt = select(Product).where(Product.search_vector.op("@@")(ts_query)).options(selectinload(Product.category))
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
    

    async def get_all(
            self,
            category_id: int | None = None,
            skip: int = 0,
            limit: int = 20,
    ) -> list[Product]:
        stmt = (select(Product)
                .options(selectinload(Product.category), selectinload(Product.variants))
                .order_by(Product.id)
        )

        if category_id is not None:
            stmt = stmt.where(Product.category_id == category_id)

        stmt = stmt.offset(skip).limit(limit)
        
        result = await self.session.execute(stmt)
        return result.scalars().all()


    async def get_by_id(self, product_id: int) -> Product:
        stmt = select(Product).where(Product.id == product_id).options(selectinload(Product.category), selectinload(Product.variants))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


    async def get_by_slug(self, slug: str) -> Product:
        stmt = select(Product).where(Product.slug == slug).options(selectinload(Product.category), selectinload(Product.variants))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


    async def create(self, product: Product) -> Product:
        self.session.add(product)
        await self.session.flush()

        stmt = (
            select(Product)
            .where(Product.id == product.id)
            .options(selectinload(Product.category), selectinload(Product.variants))
            .execution_options(populate_existing=True)
        )
        result = await self.session.execute(stmt)

        return result.scalar_one()


    async def slug_exists(self, slug: str) -> bool:
        stmt = select(Product.id).where(Product.slug == slug)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None


    async def update(self, product: Product) -> Product:
        await self.session.flush()

        stmt = (
            select(Product)
            .where(Product.id == product.id)
            .options(selectinload(Product.category), selectinload(Product.variants))
            .execution_options(populate_existing=True)
        )
        result = await self.session.execute(stmt)

        return result.scalar_one()


    async def delete(self, product: Product) -> None:
        await self.session.delete(product)
        await self.session.flush()