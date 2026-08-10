from app.exceptions import NotFoundError, ValidationError, ConflictError


class PromoCodeNotFoundError(NotFoundError):
    def __init__(self):
        super().__init__(f"Promo code not found")


class PromoCodeExpiredError(ValidationError):
    def __init__(self, code: str):
        self.code = code
        super().__init__(f"Promo code {code} was expired")


class PromoCodeUsageLimitExceededError(ValidationError):
    def __init__(self, code: str):
            self.code = code
            super().__init__(f"Usage limit of {code} was exceeded")


class PromoCodeMinOrderAmountError(ValidationError):
     def __init__(self):
        super().__init__(f"Order minimum error")


class PromoCodeValidationError(ValidationError):
    def __init__(self, code: str):
        self.code = code
        super().__init__(f"Invalid promo code {code}")


class PromoCodeAlreadyExists(ConflictError):
    def __init__(self, code: str):
        self.code = code
        super().__init__(f"Promo code {code} already exists")