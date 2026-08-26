from slugify import slugify
from sqlalchemy import func, update

from app.repositories import ProductRepository, DiscountRepository
from app.database import (
    ProductCreate, Product, ProductUpdate, 
    ProductVariant, ProductVariantPublicResponse, 
    ProductResponse, CategoryShort,
    )
from app.exceptions import ProductNotFoundSlugError, ProductNotFoundError
from app.core.pricing import calculate_final_price
from app.core.discount_resolver import resolve_final_prices


class ProductService:

    def __init__(self, repo: ProductRepository, discount_repo: DiscountRepository):
        self.repo = repo
        self.discount_repo = discount_repo


    async def _build_variant_responses(
            self, variants: list[ProductVariant],
    ) -> list[ProductVariantPublicResponse]:
        if not variants:
            return []

        final_prices = await resolve_final_prices(variants=variants, discount_repo=self.discount_repo)

        result = []
        for variant in variants:
            result.append(
                ProductVariantPublicResponse(
                    id=variant.id,
                    product_id=variant.product_id,
                    name=variant.name,
                    description=variant.description,
                    price=variant.price,
                    final_price=final_prices[variant.id],
                    in_stock=variant.in_stock,
                    created_at=variant.created_at,
                    updated_at=variant.updated_at,
                )
            )
        return result


    async def _build_product_response(self, product: Product) -> ProductResponse:
        variant_responses = await self._build_variant_responses(variants=product.variants)
        return ProductResponse(
            id=product.id,
            name=product.name,
            description=product.description,
            category=CategoryShort.model_validate(product.category),
            slug=product.slug,
            variants=variant_responses,
            created_at=product.created_at,
            updated_at=product.updated_at,
        )


    async def search_products(self, query: str) -> list[Product]:
        if not query or not query.strip():
            return []
        return await self.repo.search(query=query.strip())


    async def get_product(self, product_id: int) -> Product:
        product = await self.repo.get_by_id(product_id=product_id)
        if product is None:
            raise ProductNotFoundError(product_id)
        return await self._build_product_response(product=product)


    async def get_product_by_slug(self, slug: str) -> Product:
        product = await self.repo.get_by_slug(slug=slug)
        if product is None:
            raise ProductNotFoundSlugError(slug=slug)
        return await self._build_product_response(product=product)


    async def get_all_products(
            self, 
            category_id: int | None = None,
            skip: int = 0,
            limit: int = 20,
    ) -> list[Product]:
        products = await self.repo.get_all(
            category_id=category_id,
            skip=skip,
            limit=limit,
        )
        return [await self._build_product_response(p) for p in products]


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
        return await self._build_product_response(product=product)


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
        return await self._build_product_response(product=product)


    async def delete_product(self, product_id: int) -> None:
        product = await self.get_product(product_id=product_id)
        await self.repo.delete(product=product)