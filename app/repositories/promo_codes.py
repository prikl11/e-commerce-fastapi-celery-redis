from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import PromoCode


class PromoCodeRepository:

    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_all(self, skip: int = 0, limit: int = 20) -> list[PromoCode]:
        stmt = (
            select(PromoCode)
            .offset(skip).limit(limit)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())


    async def get_by_id(self, code_id: int) -> PromoCode | None:
        return await self.session.get(PromoCode, code_id)


    async def get_by_code(self, code: str) -> PromoCode | None:
        stmt = (
            select(PromoCode).where(PromoCode.code == code)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


    async def code_exists(self, code: str) -> bool:
        return await self.get_by_code(code=code) is not None


    async def create(self, code: PromoCode) -> PromoCode:
        self.session.add(code)
        await self.session.flush()
        return code


    async def update(self, code: PromoCode) -> PromoCode:
        await self.session.flush()
        return code


    async def delete(self, code: PromoCode) -> None:
        await self.session.delete(code)
        await self.session.flush()