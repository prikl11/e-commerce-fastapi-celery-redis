from pydantic import BaseModel, model_validator
from datetime import datetime
from decimal import Decimal

from app.database import DiscountType


class PromoCodeBase(BaseModel):
    code: str
    discount: Decimal
    discount_type: DiscountType
    usage_limit: int | None = None
    usage_count: int 
    min_order_amount: Decimal | None = None
    starts_at: datetime | None = None
    expires_at: datetime | None = None

    @model_validator(mode="after")
    def check_dates(self):
        if self.starts_at and self.expires_at and self.expires_at <= self.starts_at:
            raise ValueError("expires_at must be after starts_at")
        return self


class PromoCodeCreate(PromoCodeBase):
    pass 


class PromoCodeUpdate(BaseModel):
    discount: Decimal | None = None
    discount_type: DiscountType | None = None
    usage_limit: int | None = None
    usage_count: int  | None = None
    min_order_amount: Decimal | None = None
    starts_at: datetime | None = None
    expires_at: datetime | None = None

    @model_validator(mode="after")
    def check_dates(self):
        if self.starts_at and self.expires_at and self.expires_at <= self.starts_at:
            raise ValueError("expires_at must be after starts_at")
        return self


class PromoCodeResponse(PromoCodeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}