import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from httpx import AsyncClient, ASGITransport
from decimal import Decimal
from unittest.mock import patch

from app.core.config import settings
from app.database.base import Base
from app.database.db import get_db
from app.main import app
from app.database import Category, Product, ProductVariant


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_db():
    async_engine = create_async_engine(settings.test_database_url)
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield async_engine
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await async_engine.dispose()


@pytest_asyncio.fixture()
async def db_session(setup_db):
    async_session = async_sessionmaker(
        bind=setup_db,
        autoflush=False,
        autocommit=False,
    )
    async with async_session() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture()
async def client(db_session):
    async def override_get_session():
        yield db_session

    app.dependency_overrides[get_db] = override_get_session

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest_asyncio.fixture()
async def sample_variant(db_session):
    category = Category(name="Test Category", slug="test-category")
    db_session.add(category)
    await db_session.flush()

    product = Product(name="Test Product", category_id=category.id, slug="test-product")
    db_session.add(product)
    await db_session.flush()

    variant = ProductVariant(product_id=product.id, name="Default", price=Decimal("100.00"), stock_quantity=10)
    db_session.add(variant)
    await db_session.flush()

    return variant


@pytest_asyncio.fixture()
async def auth_headers(client):
    await client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "password",
        "first_name": "test",
        "last_name": "user",
        "phone": "+79494399493",
    })

    login_response = await client.post("/auth/login", data={
        "username": "test@example.com",
        "password": "password"
    })
    access_token = login_response.json()["access_token"]

    return {"Authorization": f"Bearer {access_token}"}


@pytest_asyncio.fixture()
async def address_id(client, auth_headers):
    response = await client.post(
        "/addresses/",
        json={
            "city": "Москва",
            "street": "Пушкина",
            "postal_code": "122241",
            "country": "Российская Федерация",
        },
        headers=auth_headers,
    )
    return response.json()["id"]


@pytest_asyncio.fixture(autouse=True)
def mock_celery_task():
    with patch("app.tasks.orders.cancel_unpaid_order.apply_async"):
               yield