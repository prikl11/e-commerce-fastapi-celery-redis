from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import Address


class AddressRepository:

    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_all_by_user(self, user_id: int) -> list[Address]:
        stmt = (
            select(Address)
            .where(Address.user_id == user_id)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())


    async def get_by_id(self, address_id: int) -> Address | None:
        return await self.session.get(Address, address_id)


    async def get_by_id_and_user(
            self, address_id: int, user_id: int
    ) -> Address | None:
        stmt = (
            select(Address)
            .where(
                Address.id == address_id,
                Address.user_id == user_id,
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


    async def create(self, data: Address) -> Address:
        self.session.add(data)
        await self.session.flush()
        return data


    async def update(self, data: Address) -> Address:
        await self.session.flush()
        await self.session.refresh(data)
        return data


    async def delete(self, data: Address) -> None:
        await self.session.delete(data)