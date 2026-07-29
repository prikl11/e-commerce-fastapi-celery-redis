from pydantic import BaseModel, model_validator
from datetime import datetime
from decimal import Decimal

from app.database import DiscountType


class DiscountBase(BaseModel):
    discount: Decimal
    discount_type: DiscountType
    variant_id: int | None = None
    category_id: int | None = None
    starts_at: datetime | None = None
    expires_at: datetime | None = None

    @model_validator(mode="after")
    def check_target_exclusive(self):
        if (self.variant_id is None) == (self.category_id is None):
            raise ValueError(
                "Exactly one of variant_id or category_id must be set"
            )
        return self

    @model_validator(mode="after")
    def check_dates(self):
        if self.starts_at and self.expires_at and self.expires_at <= self.starts_at:
            raise ValueError("expires_at must be after starts_at")
        return self


class DiscountCreate(DiscountBase):
    pass 


class DiscountUpdate(BaseModel):
    discount: Decimal | None = None
    discount_type: DiscountType | None = None
    starts_at: datetime | None = None
    expires_at: datetime | None = None

    @model_validator(mode="after")
    def check_dates(self):
        if self.starts_at and self.expires_at and self.expires_at <= self.starts_at:
            raise ValueError("expires_at must be after starts_at")
        return self    


class DiscountResponse(DiscountBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}