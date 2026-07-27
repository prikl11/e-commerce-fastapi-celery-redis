from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import func, String, Text, ForeignKey, DateTime, Numeric
from decimal import Decimal
from datetime import datetime

from app.database import Base


class ProductVariant(Base):
    __tablename__ = "product_variants"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(120))
    description: Mapped[str | None] = mapped_column(Text)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    stock_quantity: Mapped[int] = mapped_column(server_default="0")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(),
    )

    product: Mapped["Product"] = relationship(back_populates="variants")
    cart_items: Mapped[list["CartItem"]] = relationship(back_populates="variant")
    discounts: Mapped[list["Discount"]] = relationship(back_populates="variant")
    order_items: Mapped[list["OrderItem"]] = relationship("variant")