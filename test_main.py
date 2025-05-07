import pytest
import pytest_asyncio

from httpx import AsyncClient

BASE_URL = "http://127.0.0.1:8000"

@pytest_asyncio.fixture(scope="session")
async def test_user():
    user_data = {
        "email": "test_case@example.com",
        "password": "Test123",
        "full_name": "Test Case"
    }
    async with AsyncClient(base_url=BASE_URL) as client:
        registration_response = await client.post("/auth/register", json=user_data)
        assert registration_response.status_code == 201
        assert registration_response.json()['full_name'] == "Test Case"
        assert registration_response.json()['email'] == "test_case@example.com"

    yield user_data

    login_data = {
        "username": user_data["email"],
        "password": user_data["password"],
    }
    async with AsyncClient(base_url=BASE_URL) as client:
        login_response = await client.post("/auth/jwt/login", data=login_data)
        assert login_response.status_code == 200

        access_token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        delete_response = await client.delete("/users-delete/", headers=headers)
        assert delete_response.status_code == 204


@pytest.mark.anyio
async def test_register_unsuccessful(test_user):
    user_data = {
        "email": test_user["email"],
        "password": "Some_Password123",
        "full_name": "Some Full Name"
    }

    async with AsyncClient(base_url=BASE_URL) as client:
        registration_response = await client.post("/auth/register", json=user_data)
        assert registration_response.status_code == 400
        assert registration_response.json()["detail"] == "REGISTER_USER_ALREADY_EXISTS"


@pytest.mark.anyio
async def test_login(test_user):
    login_data = {
        "username": test_user["email"],
        "password": test_user["password"]
    }
    async with AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/auth/jwt/login", data=login_data)
        assert response.status_code == 200
        assert response.json()["token_type"] == "bearer"
    return response.json()["access_token"]


@pytest.mark.anyio
async def test_login_unsuccessful(test_user):
    login_data = {
        "username": "wrong_test_case@example.com",
        "password": test_user["password"]
    }
    async with AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/auth/jwt/login", data=login_data)
        assert response.status_code == 400
        assert response.json()["detail"] == "LOGIN_BAD_CREDENTIALS"


@pytest.mark.anyio
async def test_get_user_info(test_user):
    access_token = await test_login(test_user)
    
    async with AsyncClient(base_url=BASE_URL) as client:
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        response = await client.get("/users/me", headers=headers)
        assert response.status_code == 200
        assert response.json()["email"] == "test_case@example.com"
        assert response.json()["full_name"] == "Test Case"


@pytest.mark.anyio
async def test_get_user_info_unsuccessful(test_user):
    async with AsyncClient(base_url=BASE_URL) as client:
        headers = {
            "Authorization": f"Bearer WRONG TOKEN"
        }
        response = await client.get("/users/me", headers=headers)
        assert response.status_code == 401
        assert response.json()["detail"] == "Unauthorized"


@pytest.mark.anyio
async def test_update_user_info(test_user):
    access_token = await test_login(test_user)

    updated_user_data = {
        "full_name": "Test Case Updated",
        "email": "test_case_updated@example.com"
    }
    async with AsyncClient(base_url=BASE_URL) as client:
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        response = await client.patch(url="/users/me", json=updated_user_data, headers=headers)
        assert response.status_code == 200
        assert response.json()["full_name"] == "Test Case Updated"
        assert response.json()["email"] == "test_case_updated@example.com"


    updated_user_data = {
        "full_name": "Test Case",
        "email": "test_case@example.com"
    }
    async with AsyncClient(base_url=BASE_URL) as client:
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        response = await client.patch(url="/users/me", json=updated_user_data, headers=headers)
        assert response.status_code == 200
        assert response.json()["full_name"] == "Test Case"
        assert response.json()["email"] == "test_case@example.com"





@pytest.mark.anyio
async def test_categories():
    async with AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/categories")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

