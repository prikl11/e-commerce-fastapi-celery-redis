from app.database import OrderStatus, PaymentStatus
from app.exceptions import InvalidOrderStatusTransitionError, InvalidPaymentStatusTransitionError


ORDER_STATUS_TRANSITIONS: dict[OrderStatus, set[OrderStatus]] = {
    OrderStatus.created: {OrderStatus.processing, OrderStatus.cancelled},
    OrderStatus.processing: {OrderStatus.shipped, OrderStatus.cancelled},
    OrderStatus.shipped: {OrderStatus.delivered,},
    OrderStatus.delivered: set(),
    OrderStatus.cancelled: set(),
}

PAYMENT_STATUS_TRANSITIONS: dict[PaymentStatus, set[PaymentStatus]] = {
    PaymentStatus.pending: {PaymentStatus.paid, PaymentStatus.failed},
    PaymentStatus.paid: {PaymentStatus.refunded,},
    PaymentStatus.failed: set(),
    PaymentStatus.refunded:  set(),
}


def validate_order_status_transition(
        current: OrderStatus, new: OrderStatus,
) -> None:
    if new not in ORDER_STATUS_TRANSITIONS[current]:
        raise InvalidOrderStatusTransitionError(current, new)


def validate_payment_status_transition(
        current: PaymentStatus, new: PaymentStatus,
) -> None:
    if new not in PAYMENT_STATUS_TRANSITIONS[current]:
        raise InvalidPaymentStatusTransitionError(current, new)