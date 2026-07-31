from app.exceptions import NotFoundError, ConflictError, ValidationError


class ProductVarianNotFoundError(NotFoundError):
    def __init__(self, category_id: int):
        self.category_id = category_id
        super().__init__(f"Product with id={category_id} not found")


class ProductVariantNotFoundSlugError(NotFoundError):
    def __init__(self, slug: str):
        self.slug = slug
        super().__init__(f"Product with slug='{slug}' not found")


class ProductVariantSlugConflictError(ConflictError):
    def __init__(self, slug: str):
        self.slug = slug
        super().__init__(f"Product with slug='{slug}' already exists")


class InsufficientStockError(ValidationError):
    def __init__(
            self,
            variant_id: int,
            requested: int,
            available: int,
    ):
        self.variant_id = variant_id
        super().__init__(
            f"Insufficient stock for variant {variant_id}: "
            f"requested {requested}, available {available}"
        )