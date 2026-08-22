from app.exceptions import NotFoundError


class AddressNotFoundError(NotFoundError):
    def __init__(self):
        super().__init__("Address not found")