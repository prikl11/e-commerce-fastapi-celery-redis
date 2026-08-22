from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal


class ProductVariantBase(BaseModel):
    name: str
    description: str | None = None
    price: Decimal
    stock_quantity: int


class ProductVariantCreate(ProductVariantBase):
    pass


class ProductVariantUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: Decimal | None = None
    stock_quantity: int | None = None


class ProductVariantPublicResponse(BaseModel):
    id: int
    product_id: int
    name: str
    description: str | None = None
    price: Decimal
    final_price: Decimal
    in_stock: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ProductVariantAdminResponse(ProductVariantBase):
    id: int
    product_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class StockAdjustment(BaseModel):
    delta: int