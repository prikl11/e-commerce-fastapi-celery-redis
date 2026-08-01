from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import User, UserRole


class UserRepository:

    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_all(
            self,
            skip: int = 0,
            limit: int = 20,
    ) -> list[User]:
        stmt = (
            select(User)
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())


    async def get_by_role(
            self,
            role: UserRole,
            skip: int = 0,
            limit: int = 20,
    ) -> list[User]:
        stmt = (
            select(User).where(User.role == role)
            .offset(skip).limit(limit)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())


    async def get_by_id(self, user_id: int) -> User | None:
        return await self.session.get(User, user_id)


    async def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


    async def get_by_phone(self, phone: str) -> User | None:
        stmt = select(User).where(User.phone == phone)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


    async def change_role(
            self,
            user: User,
            role: UserRole,
    ) -> User:
        user.role = role
        await self.session.flush()

        stmt = (
            select(User)
            .where(User.id == user.id)
            .execution_options(populate_existing=True)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one()


    async def create(self, data: User) -> User:
        self.session.add(data)
        await self.session.flush()

        stmt = (
            select(User)
            .where(User.id == data.id)
            .execution_options(populate_existing=True)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one()


    async def update(self, data: User) -> User:
        await self.session.flush()

        stmt = (
            select(User)
            .where(User.id == data.id)
            .execution_options(populate_existing=True)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one()


    async def delete(self, data: User) -> None:
        await self.session.delete(data)
        await self.session.flush()


    async def email_exists(self, email: str) -> bool:
        stmt = select(User.id).where(User.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None


    async def phone_exists(self, phone: str) -> bool:
        stmt = select(User.id).where(User.phone == phone)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None