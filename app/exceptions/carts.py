from app.exceptions import NotFoundError, ConflictError


class CartNotFoundError(NotFoundError):
    def __init__(self, cart_id: int):
        self.cart_id = cart_id
        super().__init__(f"Cart with id={cart_id} not found")


class EmptyCartError(ConflictError):
    def __init__(self):
        super().__init__("The cart is empty")