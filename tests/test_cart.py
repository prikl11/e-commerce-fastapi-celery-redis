import pytest


async def test_add_item_to_cart(client, sample_variant, auth_headers):
    response = await client.post("/carts/items", json={
        "variant_id": sample_variant.id,
        "quantity": 1,
    }, headers=auth_headers
    )

    assert response.status_code == 201


async def test_add_same_item_twice_increases_quantity(client, sample_variant, auth_headers):
    await client.post(
        "/carts/items",
        json={"variant_id": sample_variant.id, "quantity": 1},
        headers=auth_headers,
    )
    response = await client.post(
        "/carts/items",
        json={"variant_id": sample_variant.id, "quantity": 1},
        headers=auth_headers,
    )

    assert response.json()["items"][0]["quantity"] == 2


async def test_add_item_insufficient_stock(client, sample_variant, auth_headers):
    response = await client.post(
        "/carts/items",
        json={"variant_id": sample_variant.id, "quantity": 11},
        headers=auth_headers,
    )
    assert response.status_code == 422
    assert "InsufficientStock" in response.json()["detail"] or "insufficient" in response.json()["detail"].lower()


async def test_remove_item_from_cart(client, sample_variant, auth_headers):
    await client.post(
        "/carts/items",
        json={"variant_id": sample_variant.id, "quantity": 1},
        headers=auth_headers,
    )
    await client.delete(
        f"/carts/items/{sample_variant.id}",
        headers=auth_headers
    )

    response = await client.get(
        "/carts/me",
        headers=auth_headers
    )
    print(response.json())
    assert response.json()["items"] == []


async def test_cart_isolated_per_user(client, sample_variant, auth_headers):
    await client.post(
        "/carts/items",
        json={"variant_id": sample_variant.id, "quantity": 1},
        headers=auth_headers,
    )

    await client.post("/auth/register", json={
        "email": "second@example.com",
        "password": "password",
        "first_name": "Second",
        "last_name": "User",
        "phone": "+79991234567",
    })
    login_response = await client.post("/auth/login", data={
        "username": "second@example.com",
        "password": "password",
    })
    second_user_token = login_response.json()["access_token"]
    second_auth_headers = {"Authorization": f"Bearer {second_user_token}"}

    response = await client.get("/carts/me", headers=second_auth_headers)
    assert response.json()["items"] == []