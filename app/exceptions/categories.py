from app.exceptions import NotFoundError, ConflictError


class CategoryNotFoundError(NotFoundError):
    def __init__(self, category_id: int):
        self.category_id = category_id
        super().__init__(f"Category with id={category_id} not found")


class CategoryNotFoundSlugError(NotFoundError):
    def __init__(self, slug: str):
        self.slug = slug
        super().__init__(f"Category with slug='{slug}' not found")


class CategorySlugConflictError(ConflictError):
    def __init__(self, slug: str):
        self.slug = slug
        super().__init__(f"Category with slug='{slug}' already exists")