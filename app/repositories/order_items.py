from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import OrderItem


class OrderItemRepository:

    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_all_by_order(self, order_id: int) -> list[OrderItem]:
        stmt = (
            select(OrderItem)
            .options(selectinload(OrderItem.variant))
            .where(OrderItem.order_id == order_id)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())


    async def create(self, data: OrderItem) -> OrderItem:
        self.session.add(data)
        await self.session.flush()

        stmt = (
            select(OrderItem)
            .options(selectinload(OrderItem.variant))
            .where(OrderItem.id == data.id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one()