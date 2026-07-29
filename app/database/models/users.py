from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, func
from datetime import datetime

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(60))
    last_name: Mapped[str] = mapped_column(String(80))
    phone: Mapped[str | None] = mapped_column(String(30), unique=True, nullable=True)
    email: Mapped[str] = mapped_column(String(80), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    addresses: Mapped[list["Address"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    carts: Mapped[list["Cart"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    orders: Mapped[list["Order"]] = relationship(back_populates="user")