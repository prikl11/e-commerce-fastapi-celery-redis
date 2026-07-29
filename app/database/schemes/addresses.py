from pydantic import BaseModel
from datetime import datetime


class AddressBase(BaseModel):
    user_id: int
    city: str
    street: str
    postal_code: str
    country: str


class AddressCreate(AddressBase):
    pass


class AddressUpdate(BaseModel):
    city: str | None = None
    street: str | None = None
    postal_code: str | None = None
    country: str | None = None


class AddressResponse(AddressBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}