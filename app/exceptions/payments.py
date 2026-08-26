from app.database import PaymentStatus
from app.exceptions import ValidationError


class InvalidPaymentStatusTransitionError(ValidationError):
    def __init__(self, current: PaymentStatus, new: PaymentStatus):
        super().__init__(f"Cannot transition payment from {current} to {new}")