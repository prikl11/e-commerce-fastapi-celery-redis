from pydantic import BaseModel
from datetime import datetime

from app.database.schemes import CategoryShort
from app.database.schemes.product_variants import ProductVariantPublicResponse


class ProductBase(BaseModel):
    name: str
    description: str | None = None
    category_id: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    category_id: int | None = None


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    category: CategoryShort
    slug: str
    variants: list[ProductVariantPublicResponse]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}