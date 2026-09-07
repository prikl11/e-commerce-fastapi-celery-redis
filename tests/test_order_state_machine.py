import pytest

from app.core.order_state_machine import validate_order_status_transition, validate_payment_status_transition
from app.database import OrderStatus, PaymentStatus
from app.exceptions import InvalidOrderStatusTransitionError, InvalidPaymentStatusTransitionError


def test_valid_transition_created_to_processing():
    validate_order_status_transition(OrderStatus.created, OrderStatus.processing)


def test_invalid_transition_delivered_to_created():
    with pytest.raises(InvalidOrderStatusTransitionError):
        validate_order_status_transition(OrderStatus.delivered, OrderStatus.created)


def test_valid_transition_pending_to_paid():
    validate_payment_status_transition(PaymentStatus.pending, PaymentStatus.paid)


def test_valid_transition_pending_to_failed():
    validate_payment_status_transition(PaymentStatus.pending, PaymentStatus.failed)


def test_invalid_transition_failed_to_paid():
    with pytest.raises(InvalidPaymentStatusTransitionError):
        validate_payment_status_transition(PaymentStatus.failed, PaymentStatus.paid)


def test_invalid_transition_paid_to_pending():
    with pytest.raises(InvalidPaymentStatusTransitionError):
        validate_payment_status_transition(PaymentStatus.paid, PaymentStatus.pending)


def test_valid_transition_paid_to_refunded():
    validate_payment_status_transition(PaymentStatus.paid, PaymentStatus.refunded)


def test_invalid_transition_created_to_shipped():
    with pytest.raises(InvalidOrderStatusTransitionError):
        validate_order_status_transition(OrderStatus.created, OrderStatus.shipped)