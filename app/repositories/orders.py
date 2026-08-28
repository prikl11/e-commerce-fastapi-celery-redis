from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import Order, OrderStatus, OrderItem


class OrderRepository:

    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_all(
            self, 
            user_id: int | None = None,
            status: OrderStatus | None = None,
            skip: int = 0, 
            limit: int = 20,
    ) -> list[Order]:
        query = (
            select(Order)
            .options(selectinload(Order.items).selectinload(OrderItem.variant),
                    selectinload(Order.user)
            )
        )
        if user_id is not None:
            query = query.where(Order.user_id == user_id)
        if status is not None:
            query = query.where(Order.status == status)
        stmt = query.offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())


    async def get_by_id(self, order_id: int) -> Order | None:
        stmt = (
            select(Order)
            .options(selectinload(Order.items).selectinload(OrderItem.variant),
                    selectinload(Order.user)
            )
            .where(Order.id == order_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


    async def create(self, data: Order) -> Order:
        self.session.add(data)
        await self.session.flush()

        stmt = (
            select(Order)
            .options(selectinload(Order.items).selectinload(OrderItem.variant),
                    selectinload(Order.user)
            )
            .where(Order.id == data.id)
            .execution_options(populate_existing=True)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one()


    async def update(self, data: Order) -> Order:
        await self.session.flush()

        stmt = (
            select(Order)
            .options(selectinload(Order.items).selectinload(OrderItem.variant),
                    selectinload(Order.user)
            )
            .where(Order.id == data.id)
            .execution_options(populate_existing=True)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one()