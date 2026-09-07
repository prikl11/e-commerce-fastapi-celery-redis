import pytest
from unittest.mock import patch


async def test_create_order_from_cart_success(
        client, sample_variant, auth_headers, address_id, mock_celery_task
):
    await client.post(
        "/carts/items",
        json={"variant_id": sample_variant.id, "quantity": 1},
        headers=auth_headers,
    )
    response = await client.post(
        "/orders/",
        json={"shipping_address_id": address_id},
        headers=auth_headers
    )
    assert response.status_code == 201


async def test_create_order_from_empty_cart(client, auth_headers, address_id, mock_celery_task):
    await client.get(
        "/carts/me",
        headers=auth_headers,
    )
    response = await client.post(
        "/orders/",
        json={"shipping_address_id": address_id},
        headers=auth_headers
    )
    assert "EmptyCart" in response.json()["detail"] or "empty" in response.json()["detail"].lower()


async def test_create_order_insufficient_stock(
        client, sample_variant, auth_headers, address_id, mock_celery_task, db_session
):
    await client.post(
        "/carts/items",
        json={"variant_id": sample_variant.id, "quantity": 1},
        headers=auth_headers,
    )

    sample_variant.stock_quantity = 0
    await db_session.flush()

    response = await client.post(
        "/orders/",
        json={"shipping_address_id": address_id},
        headers=auth_headers,
    )

    assert response.status_code == 422


async def register_and_login(client, email: str) -> dict:
    await client.post("/auth/register", json={
        "email": email, "password": "password",
        "first_name": "Test", "last_name": "User", "phone": "+79991234567",
    })
    login_response = await client.post("/auth/login", data={"username": email, "password": "password"})
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


async def test_cancel_order_restores_stock(
    client, sample_variant, auth_headers, address_id, mock_celery_task, db_session
):
    initial_stock = sample_variant.stock_quantity

    await client.post(
        "/carts/items",
        json={"variant_id": sample_variant.id, "quantity": 1},
        headers=auth_headers,
    )
    order_response = await client.post(
        "/orders/",
        json={"shipping_address_id": address_id},
        headers=auth_headers,
    )
    order_id = order_response.json()["order"]["id"]

    cancel_response = await client.post(
        f"/orders/me/{order_id}/cancel",
        json={"reason": "changed my mind"},
        headers=auth_headers,
    )
    assert cancel_response.status_code == 200
    assert cancel_response.json()["status"] == "cancelled"

    await db_session.refresh(sample_variant)
    assert sample_variant.stock_quantity == initial_stock
    

async def test_cancel_order_wrong_owner(
    client, sample_variant, auth_headers, address_id, mock_celery_task,
):
    await client.post(
        "/carts/items",
        json={"variant_id": sample_variant.id, "quantity": 1},
        headers=auth_headers,
    )
    order_response = await client.post(
        "/orders/",
        json={"shipping_address_id": address_id},
        headers=auth_headers,
    )
    order_id = order_response.json()["order"]["id"]

    other_user_headers = await register_and_login(client, "other_owner@example.com")

    response = await client.post(
        f"/orders/me/{order_id}/cancel",
        json={"reason": "not mine"},
        headers=other_user_headers,
    )
    assert response.status_code == 404


async def test_concurrent_orders_race_condition(
    client, sample_variant, auth_headers, address_id, mock_celery_task, db_session
):
    sample_variant.stock_quantity = 1
    await db_session.flush()

    await client.post(
        "/carts/items",
        json={"variant_id": sample_variant.id, "quantity": 1},
        headers=auth_headers,
    )

    second_headers = await register_and_login(client, "racer@example.com")
    await client.post(
        "/carts/items",
        json={"variant_id": sample_variant.id, "quantity": 1},
        headers=second_headers,
    )

    import asyncio
    responses = await asyncio.gather(
        client.post("/orders/", json={"shipping_address_id": address_id}, headers=auth_headers),
        client.post("/orders/", json={"shipping_address_id": address_id}, headers=second_headers),
        return_exceptions=True,
    )

    statuses = [r.status_code for r in responses if not isinstance(r, Exception)]
    assert statuses.count(201) == 1
    assert 422 in statuses or len(statuses) == 1