from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
import pytest

from main import app


@pytest.fixture()
async def test_user():
    user_data = {
        "email": "test_case@example.com",
        "password": "Test123",
        "full_name": "Test Case"
    }
    async with AsyncClient(transport=ASGITransport(app), base_url="http://127.0.0.1:8000") as client:
        response = await client.post("/auth/register", json=user_data)
    assert response.status_code == 201
    assert response.json()['full_name'] == "Test Case"
    assert response.json()['email'] == "test_case@example.com"

    yield user_data

    login_data = {
        "username": "test_case@example.com",
        "password": "Test123",
    }

    async with AsyncClient(transport=ASGITransport(app), base_url="http://127.0.0.1:8000") as client:
        login_response = await client.post("/auth/jwt/login", data=login_data)

    assert login_response.status_code == 200
    access_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    async with AsyncClient(transport=ASGITransport(app), base_url="http://127.0.0.1:8000") as client:
        delete_response = await client.delete(f"/users/{response.json()['id']}", headers=headers)
    
    assert delete_response.status_code == 200



@pytest.mark.anyio
async def test_login(test_user):
    data = {
        "username": test_user["email"],
        "password": test_user["password"]
    }
    async with AsyncClient(transport=ASGITransport(app), base_url="http://127.0.0.1:8000") as client:
        response = await client.post("/auth/jwt/login", data=data)

    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
