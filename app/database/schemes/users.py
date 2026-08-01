from pydantic import BaseModel, EmailStr
from datetime import datetime

from app.database import UserRole


class UserBase(BaseModel):
    first_name: str
    last_name: str
    phone: str | None = None
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None
    email: EmailStr | None = None
    password: str | None = None


class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class RoleUpdate(BaseModel):
    role: UserRole