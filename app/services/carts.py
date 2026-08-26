from app.repositories import CartRepository, ProductVariantRepository, CartItemRepository, DiscountRepository
from app.database import Cart, CartStatus, CartItemCreate, CartItem, ProductVariant, CartItemResponse, ProductVariantPublicResponse, CartResponse
from app.exceptions import CartNotFoundError, ProductVariantNotFoundError, InsufficientStockError, CartItemNotFoundError
from app.core.discount_resolver import resolve_final_prices


class CartService:

    def __init__(
            self, 
            repo: CartRepository, 
            product_repo: ProductVariantRepository,
            item_repo: CartItemRepository,
            discount_repo: DiscountRepository,
            ):
        self.repo = repo
        self.product_repo = product_repo
        self.item_repo = item_repo
        self.discount_repo = discount_repo


    async def _build_cart_item_responses(self, cart_items: list[CartItem]) -> list[CartItemResponse]:
        if not cart_items:
            return []

        variants = [item.variant for item in cart_items]
        final_prices = await resolve_final_prices(variants=variants, discount_repo=self.discount_repo)

        result = []
        for item in cart_items:
            variant = item.variant
            result.append(
                CartItemResponse(
                    cart_id=item.cart_id,
                    quantity=item.quantity,
                    variant=ProductVariantPublicResponse(
                        id=variant.id,
                        product_id=variant.product_id,
                        name=variant.name,
                        description=variant.description,
                        price=variant.price,
                        final_price=final_prices[variant.id],
                        in_stock=variant.in_stock,
                        created_at=variant.created_at,
                        updated_at=variant.updated_at,
                    ),
                )
            )
        return result


    async def _build_cart_response(self, cart: Cart) -> CartResponse:
        cart_responses = await self._build_cart_item_responses(cart_items=cart.items)
        return CartResponse(
            id=cart.id,
            user_id=cart.user_id,
            status=cart.status,
            items=cart_responses,
            created_at=cart.created_at,
            updated_at=cart.updated_at,
        )


    async def get_all(
            self,
            skip: int = 0,
            limit: int = 20,
    ) -> list[Cart]:
        carts = await self.repo.get_all(skip=skip, limit=limit)
        return carts


    async def get_all_response(
            self,
            skip: int = 0,
            limit: int = 20,
    ) -> list[CartResponse]:
        carts = await self.repo.get_all(skip=skip, limit=limit)
        return [await self._build_cart_response(c) for c in carts]


    async def get_all_by_user(
            self,
            user_id: int,
            skip: int = 0,
            limit: int = 20,
    ) -> list[Cart]:
        carts = await self.repo.get_all_by_user(
            user_id=user_id,
            skip=skip,
            limit=limit
        )
        return carts


    async def get_all_response_by_user(
            self,
            user_id: int,
            skip: int = 0,
            limit: int = 20,
    ) -> list[CartResponse]:
        carts = await self.repo.get_all_by_user(
            user_id=user_id,
            skip=skip,
            limit=limit
        )
        return [await self._build_cart_response(c) for c in carts]


    async def get_all_by_status(
            self,
            status: CartStatus = CartStatus.active,
            skip: int = 0,
            limit: int = 20,
    ) -> list[Cart]:
        carts = await self.repo.get_all_by_status(
            status=status,
            skip=skip,
            limit=limit
        )
        return carts


    async def get_all_response_by_status(
            self,
            status: CartStatus = CartStatus.active,
            skip: int = 0,
            limit: int = 20,
    ) -> list[CartResponse]:
        carts = await self.repo.get_all_by_status(
            status=status,
            skip=skip,
            limit=limit
        )
        return [await self._build_cart_response(c) for c in carts]


    async def get_all_by_user_and_status(
            self,
            user_id: int,
            status: CartStatus = CartStatus.active,
            skip: int = 0,
            limit: int = 20,
    ) -> list[Cart]:
        carts = await self.repo.get_all_by_user_and_status(
            user_id=user_id,
            status=status,
            skip=skip,
            limit=limit
        )
        return carts

    async def get_all_response_by_user_and_status(
            self,
            user_id: int,
            status: CartStatus = CartStatus.active,
            skip: int = 0,
            limit: int = 20,
    ) -> list[CartResponse]:
        carts = await self.repo.get_all_by_user_and_status(
            user_id=user_id,
            status=status,
            skip=skip,
            limit=limit
        )
        return [await self._build_cart_response(c) for c in carts]


    async def get_my_cart(self, user_id: int) -> Cart:
        cart = await self.repo.get_or_create_active_cart(user_id=user_id)
        return cart


    async def get_my_cart_response(self, user_id: int) -> CartResponse:
        cart = await self.repo.get_or_create_active_cart(user_id=user_id)
        return await self._build_cart_response(cart=cart)


    async def get_my_cart_by_id(self, user_id: int, cart_id: int) -> Cart:
        cart = await self.get_by_id(cart_id=cart_id)
        if cart.user_id != user_id:
            raise CartNotFoundError(cart_id=cart_id)
        return cart


    async def get_my_cart_response_by_id(
            self, user_id: int, cart_id: int,
    ) -> CartResponse:
        cart = await self.get_my_cart_by_id(user_id=user_id, cart_id=cart_id)
        return await self._build_cart_response(cart=cart)


    async def get_by_id(self, cart_id: int) -> Cart:
        cart = await self.repo.get_by_id(cart_id=cart_id)
        if cart is None:
            raise CartNotFoundError(cart_id=cart_id)
        return cart


    async def get_cart_response_by_id(self, cart_id: int) -> CartResponse:
        cart = await self.get_by_id(cart_id=cart_id)
        return await self._build_cart_response(cart=cart)


    async def change_status(
            self,
            cart_id: int,
            status: CartStatus,
    ) -> Cart:
        cart = await self.get_by_id(cart_id=cart_id)
        return await self.repo.change_status(cart=cart, status=status)


    async def _check_stock(self, variant_id: int, quantity: int) -> ProductVariant:
        variant = await self.product_repo.get_by_id(variant_id=variant_id)
        if variant is None:
            raise ProductVariantNotFoundError(variant_id)
        if variant.stock_quantity < quantity:
            raise InsufficientStockError(
                variant_id=variant_id,
                requested=quantity,
                available=variant.stock_quantity
            )
        return variant


    async def add_item(
            self,
            user_id: int,
            data: CartItemCreate,
    ) -> Cart:
        cart = await self.repo.get_or_create_active_cart(user_id=user_id)
        cart_item = await self.item_repo.get_by_cart_and_variant(cart_id=cart.id, variant_id=data.variant_id)
        existing_quantity = cart_item.quantity if cart_item is not None else 0
        total_quantity = existing_quantity + data.quantity
        await self._check_stock(variant_id=data.variant_id, quantity=total_quantity)
        if cart_item is None:
            cart_item = CartItem(
                cart_id=cart.id,
                variant_id=data.variant_id,
                quantity=data.quantity,
            )
            await self.item_repo.create(cart_item=cart_item)
        else:
            cart_item.quantity += data.quantity
            await self.item_repo.update(cart_item=cart_item)
        cart = await self.get_my_cart(user_id=user_id)
        return await self._build_cart_response(cart=cart)


    async def update_item_quantity(
            self,
            user_id: int,
            variant_id: int,
            new_quantity: int
    ) -> Cart:
        cart = await self.get_my_cart(user_id=user_id)
        cart_item = await self.item_repo.get_by_cart_and_variant(cart_id=cart.id, variant_id=variant_id)
        if cart_item is None:
            raise CartItemNotFoundError()
        
        await self._check_stock(variant_id=variant_id, quantity=new_quantity)
        cart_item.quantity = new_quantity
        await self.item_repo.update(cart_item=cart_item)
        cart = await self.get_my_cart(user_id=user_id)
        return await self._build_cart_response(cart=cart)


    async def remove_item(
            self,
            user_id: int,
            variant_id: int
    ) -> Cart:
        cart = await self.get_my_cart(user_id=user_id)
        cart_item = await self.item_repo.get_by_cart_and_variant(cart_id=cart.id, variant_id=variant_id)
        if cart_item is None:
            raise CartItemNotFoundError()
        await self.item_repo.delete(cart_item=cart_item)
        cart = await self.get_my_cart(user_id=user_id)
        return await self._build_cart_response(cart=cart)