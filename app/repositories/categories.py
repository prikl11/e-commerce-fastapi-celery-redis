from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database.models import Category


class CategoryRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, category_id: int) -> Category | None:
        return await self.session.get(Category, category_id)

    async def get_by_slug(self, slug: str) -> Category | None:
        stmt = select(Category).where(Category.slug == slug)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self, parent_id: int | None = None) -> list[Category]:
        stmt = select(Category)
        if parent_id is not None:
            stmt = stmt.where(Category.parent_id == parent_id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def create(self, category: Category) -> Category:
        self.session.add(category)
        await self.session.flush()
        return category

    async def slug_exists(self, slug: str) -> bool:
        stmt = select(Category.id).where(Category.slug == slug)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None

    async def update(self, category: Category) -> Category:
        await self.session.flush()
        return category

    async def delete(self, category: Category) -> None:
        await self.session.delete(category)
        await self.session.flush()