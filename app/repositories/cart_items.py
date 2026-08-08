from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import CartItem

class CartItemRepository:

    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_all_by_cart(
            self,
            cart_id: int,
    ) -> list[CartItem]:
        stmt = (
            select(CartItem)
            .options(selectinload(CartItem.variant))
            .where(CartItem.cart_id == cart_id)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())


    async def get_by_cart_and_variant(
            self,
            cart_id: int,
            variant_id: int,
    ) -> CartItem | None:
        stmt = (
            select(CartItem)
            .options(selectinload(CartItem.variant))
            .where(CartItem.cart_id == cart_id, CartItem.variant_id == variant_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


    async def create(self, cart_item: CartItem) -> CartItem:
        self.session.add(cart_item)
        await self.session.flush()

        stmt = (
            select(CartItem)
            .options(selectinload(CartItem.variant))
            .where(CartItem.id == cart_item.id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one()


    async def update(self, cart_item: CartItem) -> CartItem:
        await self.session.flush()

        stmt = (
            select(CartItem.id == cart_item.id)
            .options(selectinload(CartItem.variant))
        )
        result = await self.session.execute(stmt)
        return result.scalar_one()


    async def delete(self, cart_item: CartItem) -> None:
        await self.session.delete(cart_item)
        await self.session.flush()