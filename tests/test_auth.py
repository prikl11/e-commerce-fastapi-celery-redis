import pytest


async def register(client, email: str | None = None, phone: str | None = None):
    if email is None:
        email = "test@example.com"
    if phone is None:
        phone = "+79991234567"

    response = await client.post("/auth/register", json={
        "email": email,
        "password": "testpassword123",
        "first_name": "test",
        "last_name": "user",
        "phone": phone,
    })
    return response


async def test_register_user(client):
    response = await register(client)

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "hashed_password" not in data
    assert "password" not in data


async def test_email_already_exists(client):
    response1 = await register(client)

    assert response1.status_code == 201

    response2 = await register(client, phone="+73994392492")

    assert response2.status_code == 409


async def test_invalid_email(client):
    response = await client.post("/auth/login", data={
        "username": "test@gmail.com",
        "password": "password",
    })

    assert response.status_code == 401


async def test_access_to_secure_endpoint_without_token(client):
    response = await client.get("/orders/")
    assert response.status_code == 401


async def test_access_admin_endpoint_as_customer(client):
    await register(client)

    login_response = await client.post("/auth/login", data={
        "username": "test@example.com",
        "password": "testpassword123"
    })
    access_token = login_response.json()["access_token"]

    response = await client.post(
        "/categories/",
        json={"name": "Test category"},
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 403