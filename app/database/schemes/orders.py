from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime

from app.database import OrderStatus, PaymentStatus
from app.database.schemes import OrderItemResponse


class OrderCreate(BaseModel):
    shipping_address_id: int
    promo_code: str | None = None


class OrderStatusUpdate(BaseModel):
    status: OrderStatus | None = None


class OrderCancel(BaseModel):
    cancellation_reason: str | None = None


class OrderResponse(BaseModel):
    id: int
    user_id: int
    status: OrderStatus
    payment_status: PaymentStatus
    total_amount: Decimal
    discount_amount: Decimal | None = None
    promo_code_id: int | None = None
    shipping_address_id: int
    items: list[OrderItemResponse]
    cancellation_reason: str | None = None
    created_at: datetime
    updated_at: datetime
    cancelled_at: datetime | None = None
    delivered_at: datetime | None = None

    model_config = {"from_attributes": True}