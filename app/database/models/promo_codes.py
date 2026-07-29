from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Numeric, Enum, DateTime, func
from datetime import datetime
from decimal import Decimal

from app.database import Base, DiscountType


class PromoCode(Base):
    __tablename__ = "promo_codes"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(30), unique=True)
    discount: Mapped[Decimal] = mapped_column(Numeric(5, 2))
    discount_type: Mapped[DiscountType] = mapped_column(Enum(DiscountType), server_default="percent")
    usage_limit: Mapped[int | None] = mapped_column()
    usage_count: Mapped[int] = mapped_column(server_default="0")
    min_order_amount: Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    starts_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(),
    )

    orders: Mapped[list["Order"]] = relationship(back_populates="promo_code")