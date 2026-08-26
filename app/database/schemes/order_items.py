from pydantic import BaseModel, computed_field
from decimal import Decimal

from app.database.schemes import ProductVariantOrderResponse


class OrderItemResponse(BaseModel):
    id: int
    variant: ProductVariantOrderResponse
    quantity: int
    price: Decimal

    model_config = {"from_attributes": True}

    @computed_field
    @property
    def subtotal(self) -> Decimal:
        return self.price * self.quantity