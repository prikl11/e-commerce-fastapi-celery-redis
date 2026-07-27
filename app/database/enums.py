import enum


class CartStatus(str, enum.Enum):
    active = "active"
    converted = "converted"
    abandoned = "abandoned"


class DiscountType(str, enum.Enum):
    percent = "percent"
    fixed = "fixed"


class OrderStatus(str, enum.Enum):
    created = "created"
    paid = "paid"
    processing = "processing"
    shipped = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"


class PaymentStatus(str, enum.Enum):
    pending = "pending"
    paid = "paid"
    failed = "failed"
    refunded = "refunded"