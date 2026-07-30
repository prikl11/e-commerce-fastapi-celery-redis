from app.exceptions import NotFoundError, ConflictError


class ProductNotFoundError(NotFoundError):
    def __init__(self, category_id: int):
        self.category_id = category_id
        super().__init__(f"Product with id={category_id} not found")


class ProductNotFoundSlugError(NotFoundError):
    def __init__(self, slug: str):
        self.slug = slug
        super().__init__(f"Product with slug='{slug}' not found")


class ProductSlugConflictError(ConflictError):
    def __init__(self, slug: str):
        self.slug = slug
        super().__init__(f"Product with slug='{slug}' already exists")