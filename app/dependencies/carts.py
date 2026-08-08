from typing import Annotated
from fastapi import Depends

from app.services import CartService
from app.repositories import CartItemRepository, CartRepository
from app.dependencies import SessionDep
from app.dependencies.product_variants import ProductVariantRepositoryDep


def get_cart_repository(db: SessionDep) -> CartRepository:
    return CartRepository(db)

CartRepositoryDep = Annotated[CartRepository, Depends(get_cart_repository)]

def get_cart_item_repository(db: SessionDep) -> CartItemRepository:
    return CartItemRepository(db)

CartItemRepositoryDep = Annotated[CartItemRepository, Depends(get_cart_item_repository)]

def get_cart_service(
        repo: CartRepositoryDep,
        product_repo: ProductVariantRepositoryDep,
        item_repo: CartItemRepositoryDep,
) -> CartService:
    return CartService(repo, product_repo, item_repo)

CartServiceDep = Annotated[CartService, Depends(get_cart_service)]