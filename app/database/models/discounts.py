from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import func, ForeignKey, Numeric, DateTime, Enum, CheckConstraint
from datetime import datetime
from decimal import Decimal

from app.database import Base, DiscountType


class Discount(Base):
    __tablename__ = "discounts"


    id: Mapped[int] = mapped_column(primary_key=True)
    discount: Mapped[Decimal] = mapped_column(Numeric(5, 2))
    discount_type: Mapped[DiscountType] = mapped_column(Enum(DiscountType), server_default="percent")
    variant_id: Mapped[int | None] = mapped_column(ForeignKey("product_variants.id", ondelete="CASCADE"))
    category_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id", ondelete="CASCADE"))
    starts_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(),
    )

    variant: Mapped["ProductVariant | None"] = relationship(back_populates="discounts")
    category: Mapped["Category | None"] = relationship(back_populates="discounts")

    __table_args__ = (
        CheckConstraint(
            "(variant_id IS NOT NULL AND category_id IS NULL) OR "
            "(variant_id IS NULL AND category_id IS NOT NULL)",
            name="check_discount_target_exclusive"
        ),
    )