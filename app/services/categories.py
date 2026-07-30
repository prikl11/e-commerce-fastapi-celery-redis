from slugify import slugify

from app.repositories import CategoryRepository
from app.database import CategoryCreate, Category, CategoryUpdate
from app.exceptions import CategoryNotFoundError, CategoryNotFoundSlugError


class CategoryService:

    def __init__(self, repo: CategoryRepository):
        self.repo = repo


    async def get_category(self, category_id: int) -> Category:
        category = await self.repo.get_by_id(category_id=category_id)
        if category is None:
            raise CategoryNotFoundError(category_id)
        return category


    async def get_category_by_slug(self, slug: str) -> Category:
        category = await self.repo.get_by_slug(slug=slug)
        if category is None:
            raise CategoryNotFoundSlugError(slug)
        return category


    async def get_all_categories(self, parent_id: int | None = None) -> list[Category]:
        return await self.repo.get_all(parent_id=parent_id)


    async def _generate_unique_slug(self, name: str) -> str:
        base_slug = slugify(name)
        slug = base_slug
        counter = 1
        while await self.repo.slug_exists(slug=slug):
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug


    async def create_category(self, data: CategoryCreate) -> Category:
        slug = await self._generate_unique_slug(data.name)
        category = Category(name=data.name, parent_id=data.parent_id, slug=slug)
        category = await self.repo.create(category=category)
        return category

    async def update_category(self, category_id: int, data: CategoryUpdate) -> Category:
        category = await self.get_category(category_id=category_id)
        if data.name is not None:
            category.name = data.name
        if data.parent_id is not None:
            category.parent_id = data.parent_id

        await self.repo.update(category=category)
        return category

    
    async def delete_category(self, category_id: int) -> None:
        category = await self.get_category(category_id=category_id)
        await self.repo.delete(category=category)