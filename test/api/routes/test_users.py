import pytest
from httpx import AsyncClient
from starlette import status


@pytest.mark.asyncio
async def test_register_user(async_client: AsyncClient) -> None:
    expected_response = {
        "email": "test@example.com",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
    }

    payload = {
        "email": "test@example.com",
        "password": "test",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "username": "Test"
    }

    response = await async_client.post("/auth/register", json=payload)
    data = response.json()

    assert response.status_code == status.HTTP_201_CREATED

    for k, v in expected_response.items():
        assert data[k] == v

    assert "id" in data


@pytest.mark.asyncio
async def test_register_user_with_false_su_and_verified_and_ensure_db_ignores(async_client: AsyncClient) -> None:
    expected_response = {
        "email": "test@example.com",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
    }

    payload = {
        "email": "test@example.com",
        "password": "test",
        "is_active": True,
        "is_superuser": True,
        "is_verified": True,
        "username": "Test"
    }

    response = await async_client.post("/auth/register", json=payload)
    data = response.json()

    assert response.status_code == status.HTTP_201_CREATED

    for k, v in expected_response.items():
        assert data[k] == v

    assert "id" in data


@pytest.mark.asyncio
async def test_jwt_login_user(async_client: AsyncClient) -> None:
    payload = {
        "email": "test@example.com",
        "password": "test",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "username": "Test"
    }

    await async_client.post("/auth/register", json=payload)

    form_data = {
        "username": "test@example.com",
        "password": "test"
    }

    response = await async_client.post("/auth/jwt/login", data=form_data)
    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_jwt_logout_user(async_client: AsyncClient) -> None:
    payload = {
        "email": "test@example.com",
        "password": "test",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "username": "Test"
    }

    await async_client.post("/auth/register", json=payload)

    form_data = {
        "username": "test@example.com",
        "password": "test"
    }

    response = await async_client.post("/auth/jwt/login", data=form_data)
    data = response.json()

    token = data["access_token"]

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = await async_client.post("/auth/jwt/logout", headers=headers)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_jwt_get_user_me(async_client: AsyncClient) -> None:
    expected_response = {
        "email": "test@example.com",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
    }

    payload = {
        "email": "test@example.com",
        "password": "test",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "username": "Test"
    }

    await async_client.post("/auth/register", json=payload)

    form_data = {
        "username": "test@example.com",
        "password": "test"
    }

    response = await async_client.post("/auth/jwt/login", data=form_data)
    data = response.json()

    token = data["access_token"]

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = await async_client.get("/users/me", headers=headers)
    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    for k, v in expected_response.items():
        assert data[k] == v

    assert "id" in data


# @pytest.mark.asyncio
# async def test_jwt_modify_user_me(async_client: AsyncClient) -> None:
#     expected_response = {
#         "email": "test2@example.com",
#         "is_active": True,
#         "is_superuser": False,
#         "is_verified": False,
#     }
#
#     payload = {
#         "email": "test@example.com",
#         "password": "test",
#         "is_active": True,
#         "is_superuser": False,
#         "is_verified": False,
#         "username": "Test"
#     }
#
#     await async_client.post("/auth/register", json=payload)
#
#     form_data = {
#         "username": "test@example.com",
#         "password": "test"
#     }
#
#     response = await async_client.post("/auth/jwt/login", data=form_data)
#     data = response.json()
#
#     token = data["access_token"]
#
#     headers = {
#         "Content-Type": "application/json",
#         "Authorization": f"Bearer {token}"
#     }
#
#     change_data = {
#         "password": "test 2",
#         "email": "test1@example.com"
#     }
#
#     # ToDo auth seems fine, but change data is broken currently (or some combination
#     response = await async_client.patch("/users/me", headers=headers, data=change_data)
#     data = response.json()
#
#     print(data)
#
#     assert response.status_code == status.HTTP_200_OK
#     for k, v in expected_response.items():
#         assert data[k] == v
#
#     assert "id" in data


# ToDo There has to be a SU designated to be able to delete a user and this has to be done by making a user SU in the db
# @pytest.mark.asyncio
# async def test_jwt_get_user_me(async_client: AsyncClient) -> None:
#     payload = {
#         "email": "test@example.com",
#         "password": "test",
#         "is_active": True,
#         "is_superuser": False,
#         "is_verified": False,
#         "username": "Test"
#     }
#
#     await async_client.post("/auth/register", json=payload)
#
#     form_data = {
#         "username": "test@example.com",
#         "password": "test"
#     }
#
#     response = await async_client.post("/auth/jwt/login", data=form_data)
#     data = response.json()
#
#     token = data["access_token"]
#
#     headers = {
#         "Content-Type": "application/json",
#         "Authorization": f"Bearer {token}"
#     }
#
#     response = await async_client.get("/users/me", headers=headers)
#     user_id = response.json()["id"]
#
#     response = await async_client.delete(f"/users/{user_id}", headers=headers)
#
#     assert response.status_code == status.HTTP_204_NO_CONTENT
