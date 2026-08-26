from app.exceptions import ValidationError, NotFoundError
from app.database import OrderStatus


class InvalidOrderStatusTransitionError(ValidationError):
    def __init__(self, current: OrderStatus, new: OrderStatus):
        super().__init__(f"Cannot transition order from {current} to {new}")


class OrderNotFoundError(NotFoundError):
    def __init__(self, order_id: int):
        super().__init__(f"Order {order_id} not found")


class OrderCannotBeCancelledError(ValidationError):
    def __init__(self, order_id: int, current_status: OrderStatus):
        super().__init__(f"Order {order_id} cannot be cancelled from status {current_status}")