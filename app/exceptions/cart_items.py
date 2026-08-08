from app.exceptions import NotFoundError


class CartItemNotFoundError(NotFoundError):
    def __init__(self):
        super().__init__("Cart item not found")