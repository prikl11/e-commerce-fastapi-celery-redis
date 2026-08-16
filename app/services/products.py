from slugify import slugify
from sqlalchemy import func, update

from app.repositories import ProductRepository, DiscountRepository
from app.database import ProductCreate, Product, ProductUpdate
from app.exceptions import ProductNotFoundSlugError, ProductNotFoundError


class ProductService:

    def __init__(self, repo: ProductRepository, discount_repo: DiscountRepository):
        self.repo = repo
        self.discount_repo = discount_repo


    async def search_products(self, query: str) -> list[Product]:
        if not query or not query.strip():
            return []
        return await self.repo.search(query=query.strip())


    async def get_product(self, product_id: int) -> Product:
        product = await self.repo.get_by_id(product_id=product_id)
        if product is None:
            raise ProductNotFoundError(product_id)
        return product


    async def get_product_by_slug(self, slug: str) -> Product:
        product = await self.repo.get_by_slug(slug=slug)
        if product is None:
            raise ProductNotFoundSlugError(slug=slug)
        return product


    async def get_all_products(
            self, 
            category_id: int | None = None,
            skip: int = 0,
            limit: int = 20,
    ) -> list[Product]:
        return await self.repo.get_all(
            category_id=category_id,
            skip=skip,
            limit=limit,
        )


    async def _generate_unique_slug(self, name: str) -> str:
        base_slug = slugify(name)
        slug = base_slug
        counter = 1
        while await self.repo.slug_exists(slug=slug):
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug

    
    async def create_product(self, data: ProductCreate) -> Product:
        slug = await self._generate_unique_slug(name=data.name)
        product = Product(**data.model_dump(), slug=slug)
        product = await self.repo.create(product=product)
        await self._update_search_vector(product)
        return product


    async def _update_search_vector(self, product: Product) -> None:
        stmt = (
            update(Product)
            .where(Product.id == product.id)
            .values(search_vector=func.to_tsvector("russian", product.name + " " + (product.description or "")))
            .execution_options(synchronize_session=False)
        )
        await self.repo.session.execute(stmt)


    async def update_product(
            self, 
            product_id: int,
            data: ProductUpdate,
    ) -> Product:
        product = await self.get_product(product_id=product_id)

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(product, key, value)

        product = await self.repo.update(product=product)
        await self._update_search_vector(product=product)
        return product


    async def delete_product(self, product_id: int) -> None:
        product = await self.get_product(product_id=product_id)
        await self.repo.delete(product=product)