from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from sqlalchemy.ext.hybrid import hybrid_property


class ProductVariantBase(BaseModel):
    product_id: int
    name: str
    description: str | None = None
    price: Decimal
    stock_quantity: int

    @hybrid_property
    def in_stock(self) -> bool:
        return self.stock_quantity > 0


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
    in_stock: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ProductVariantAdminResponse(ProductVariantBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}