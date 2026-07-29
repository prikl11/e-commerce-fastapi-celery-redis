from pydantic import BaseModel, Field, computed_field
from decimal import Decimal

from app.database.schemes import ProductVariantPublicResponse


class CartItemBase(BaseModel):
    variant_id: int
    quantity: int = Field(gt=0)


class CartItemCreate(CartItemBase):
    pass


class CartItemUpdate(BaseModel):
    quantity: int | None = Field(default=None, gt=0)


class CartItemResponse(BaseModel):
    cart_id: int
    variant: ProductVariantPublicResponse
    quantity: int

    model_config = {"from_attributes": True}

    @computed_field
    @property
    def subtotal(self) -> Decimal:
        return self.variant.price * self.quantity