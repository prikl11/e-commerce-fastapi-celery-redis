from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import Cart, CartStatus, CartItem, ProductVariant

class CartRepository:

    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_all(
            self,
            skip: int = 0,
            limit: int = 20,
    ) -> list[Cart]:
        stmt = (
            select(Cart)
            .options(
                selectinload(Cart.items)
                .selectinload(CartItem.variant)
                .selectinload(ProductVariant.product)
                )
            .offset(skip).limit(limit)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())


    async def get_all_by_user(
            self,
            user_id: int,
            skip: int = 0,
            limit: int = 20,
    ) -> list[Cart]:
        stmt = (
            select(Cart)
            .options(
                selectinload(Cart.items)
                .selectinload(CartItem.variant)
                .selectinload(ProductVariant.product)
                )
            .where(Cart.user_id == user_id)
            .offset(skip).limit(limit)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())


    async def get_all_by_status(
            self,
            status: CartStatus = CartStatus.active,
            skip: int = 0,
            limit: int = 20,
    ) -> list[Cart]:
        stmt = (
            select(Cart)
            .options(
                selectinload(Cart.items)
                .selectinload(CartItem.variant)
                .selectinload(ProductVariant.product)
                )
            .where(Cart.status == status)
            .offset(skip).limit(limit)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())


    async def get_all_by_user_and_status(
            self,
            user_id: int,
            status: CartStatus = CartStatus.active,
            skip: int = 0,
            limit: int = 20,
    ) -> list[Cart]:
        stmt = (
            select(Cart)
            .options(
                selectinload(Cart.items)
                .selectinload(CartItem.variant)
                .selectinload(ProductVariant.product)
                )
            .where(Cart.user_id == user_id, Cart.status == status)
            .offset(skip).limit(limit)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())


    async def get_active_cart(self, user_id: int) -> Cart | None:
        stmt = (
            select(Cart)
            .options(
                selectinload(Cart.items)
                .selectinload(CartItem.variant)
                .selectinload(ProductVariant.product)
                )
            .where(Cart.user_id == user_id, Cart.status == CartStatus.active)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


    async def get_by_id(self, cart_id: int) -> Cart | None:
        stmt = (
            select(Cart)
            .options(
                selectinload(Cart.items)
                .selectinload(CartItem.variant)
                .selectinload(ProductVariant.product)
                )
            .where(Cart.id == cart_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


    async def change_status(
            self,
            cart: Cart,
            status: CartStatus,
    ) -> Cart:
        cart.status = status
        await self.session.flush()

        stmt = (
            select(Cart)
            .options(
                selectinload(Cart.items)
                .selectinload(CartItem.variant)
                .selectinload(ProductVariant.product)
                )
            .where(Cart.id == cart.id)
            .execution_options(populate_existing=True)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one()


    async def create(self, cart: Cart) -> Cart:
        self.session.add(cart)
        await self.session.flush()
        stmt = (
            select(Cart)
            .options(
                selectinload(Cart.items)
                .selectinload(CartItem.variant)
                .selectinload(ProductVariant.product)
                )
            .where(Cart.id == cart.id)
            .execution_options(populate_existing=True)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one()


    async def get_or_create_active_cart(self, user_id: int) -> Cart:
        cart = await self.get_active_cart(user_id=user_id)
        if cart is None:
            cart = await self.create(cart=Cart(user_id=user_id, status=CartStatus.active))
        return cart
