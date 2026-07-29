from pydantic import BaseModel, computed_field
from decimal import Decimal

from app.database.schemes import ProductVariantPublicResponse


class OrderItemResponse(BaseModel):
    id: int
    variant: ProductVariantPublicResponse
    quantity: int
    price: Decimal

    model_config = {"from_attributes": True}

    @computed_field
    @property
    def subtotal(self) -> Decimal:
        return self.price * self.quantity