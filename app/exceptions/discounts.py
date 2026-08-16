from app.exceptions import NotFoundError, ConflictError


class DiscountNotFoundError(NotFoundError):
    def __init__(self):
        super().__init__("Discount not found")


class DiscountAlreadyExistsError(ConflictError):
    def __init__(self):
        super().__init__("Discount already exists")