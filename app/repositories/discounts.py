from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from datetime import datetime, timezone

from app.database import Discount


class DiscountRepository:

    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_all(self, skip: int = 0, limit: int = 20) -> list[Discount]:
        stmt = (
            select(Discount)
            .offset(skip).limit(limit)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())


    async def get_by_id(self, discount_id: int) -> Discount | None:
        return await self.session.get(Discount, discount_id)


    async def get_active_for_variant(self, variant_id: int) -> list[Discount]:
        now = datetime.now(timezone.utc)
        stmt = (
            select(Discount)
            .where(
                Discount.variant_id == variant_id,
                or_(Discount.starts_at.is_(None), Discount.starts_at <= now),
                or_(Discount.expires_at.is_(None), Discount.expires_at >= now),
                )
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())


    async def get_active_for_category(self, category_id: int) -> list[Discount]:
        now = datetime.now(timezone.utc)
        stmt = (
            select(Discount)
            .options(selectinload(Discount.variant))
            .where(
                Discount.category_id == category_id,
                or_(Discount.starts_at.is_(None), Discount.starts_at <= now),
                or_(Discount.expires_at.is_(None), Discount.expires_at >= now),
                )
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())


    async def get_active_for_variants_bulk(self, variant_ids: list[int]) -> list[Discount]:
        now = datetime.now(timezone.utc)
        stmt = (
            select(Discount)
            .options(selectinload(Discount.variant))
            .where(
                Discount.variant_id.in_(variant_ids),
                or_(Discount.starts_at.is_(None), Discount.starts_at <= now),
                or_(Discount.expires_at.is_(None), Discount.expires_at >= now),
                )
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())


    async def get_active_for_categories_bulk(self, category_ids: list[int]) -> list[Discount]:
        now = datetime.now(timezone.utc)
        stmt = (
            select(Discount)
            .options(selectinload(Discount.variant))
            .where(
                Discount.category_id.in_(category_ids),
                or_(Discount.starts_at.is_(None), Discount.starts_at <= now),
                or_(Discount.expires_at.is_(None), Discount.expires_at >= now),
                )
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())


    async def create(self, data: Discount) -> Discount:
        self.session.add(data)
        await self.session.flush()
        return data


    async def update(self, data: Discount) -> Discount:
        await self.session.flush()
        return data


    async def delete(self, data: Discount) -> None:
        await self.session.delete(data)
        await self.session.flush()