from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum, Numeric, DateTime, func, ForeignKey
from datetime import datetime
from decimal import Decimal

from app.database import Base, PaymentStatus, OrderStatus


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"))
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), server_default="created")
    payment_status: Mapped[PaymentStatus] = mapped_column(
        Enum(PaymentStatus), server_default="pending"
    )
    total_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    discount_amount: Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    promo_code_id: Mapped[int | None] = mapped_column(ForeignKey("promo_codes.id", ondelete="RESTRICT"))
    shipping_address_id: Mapped[int] = mapped_column(ForeignKey("addresses.id", ondelete="RESTRICT"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )    
    cancelled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    delivered_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    user: Mapped["User"] = relationship(back_populates="orders")
    promo_code: Mapped["PromoCode | None"] = relationship(back_populates="orders")
    shipping_address: Mapped["Address"] = relationship(back_populates="orders")
    items: Mapped[list["OrderItem"]] = relationship(back_populates="order", cascade="all, delete-orphan")