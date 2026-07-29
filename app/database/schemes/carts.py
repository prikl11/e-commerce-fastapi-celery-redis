from pydantic import BaseModel, computed_field
from datetime import datetime
from decimal import Decimal

from app.database import CartStatus
from app.database.schemes import CartItemResponse


class CartResponse(BaseModel):
    id: int
    user_id: int
    status: CartStatus
    items: list[CartItemResponse]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

    @computed_field
    @property
    def total(self) -> Decimal:
        return sum((item.subtotal for item in self.items), Decimal("0"))