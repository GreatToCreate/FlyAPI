import pytest
from httpx import AsyncClient
from starlette import status


user_payload = {
        "email": "test@example.com",
        "password": "test",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "username": "Test"
    }

ship_payload = {
        "description": "Test description",
        "ship_json": {
            "angularDrag": 10.0,
            "boostCapacitorPercentCost": 10.0,
            "boostCapacityPercentChargeRate": 200.0,
            "boostMaxSpeedDropOffTime": 10.2,
            "boostRechargeTime": 20.3,
            "drag": 0,
            "inertiaTensorMultiplier": 60,
            "latHMultiplier": 0,
            "latVMultiplier": 0,
            "mass": 0,
            "maxAngularVelocity": 0,
            "maxBoostSpeed": 0,
            "maxSpeed": 0,
            "maxThrust": 0,
            "minUserLimitedVelocity": 0,
            "pitchMultiplier": 0,
            "rollMultiplier": 0,
            "throttleMultiplier": 0,
            "thrustBoostMultiplier": 0,
            "torqueBoostMultiplier": 0,
            "torqueThrustMultiplier": 0,
            "totalBoostRotationalTime": 0,
            "totalBoostTime": 0,
            "yawMultiplier": 0
        },
        "name": "Test Ship"
    }

form_data = {
    "username": "test@example.com",
    "password": "test"
}


@pytest.mark.asyncio
async def test_create_ship(async_client: AsyncClient) -> None:
    await async_client.post("/auth/register", json=user_payload)

    response = await async_client.post("/auth/jwt/login", data=form_data)
    data = response.json()

    token = data["access_token"]

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = await async_client.post("/ships/", headers=headers, json=ship_payload)
    data = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert data["description"] == "Test description"
    assert data["name"] == "Test Ship"
    assert data["ship_json"]["angularDrag"] == 10.0
    assert data["ship_json"]["boostCapacitorPercentCost"] == 10.0
    assert data["ship_json"]["boostCapacityPercentChargeRate"] == 200.0
    assert data["ship_json"]["boostMaxSpeedDropOffTime"] == 10.2
    assert data["ship_json"]["boostRechargeTime"] == 20.3
    assert data["ship_json"]["inertiaTensorMultiplier"] == 60


@pytest.mark.asyncio
async def test_get_ships(async_client: AsyncClient) -> None:
    await async_client.post("/auth/register", json=user_payload)

    response = await async_client.post("/auth/jwt/login", data=form_data)
    data = response.json()

    token = data["access_token"]

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    await async_client.post("/ships/", headers=headers, json=ship_payload)

    response = await async_client.get("/ships/")
    data = response.json()

    assert len(data) == 1

    assert response.status_code == status.HTTP_200_OK

    assert data[0]["description"] == "Test description"
    assert data[0]["name"] == "Test Ship"
    assert data[0]["ship_json"]["angularDrag"] == 10.0
    assert data[0]["ship_json"]["boostCapacitorPercentCost"] == 10.0
    assert data[0]["ship_json"]["boostCapacityPercentChargeRate"] == 200.0
    assert data[0]["ship_json"]["boostMaxSpeedDropOffTime"] == 10.2
    assert data[0]["ship_json"]["boostRechargeTime"] == 20.3
    assert data[0]["ship_json"]["inertiaTensorMultiplier"] == 60


@pytest.mark.asyncio
async def test_get_ship_by_id(async_client: AsyncClient) -> None:
    await async_client.post("/auth/register", json=user_payload)

    response = await async_client.post("/auth/jwt/login", data=form_data)
    data = response.json()

    token = data["access_token"]

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    await async_client.post("/ships/", headers=headers, json=ship_payload)

    response = await async_client.get("/ships/id/1")
    data = response.json()

    assert response.status_code == status.HTTP_200_OK

    assert data["description"] == "Test description"
    assert data["name"] == "Test Ship"
    assert data["ship_json"]["angularDrag"] == 10.0
    assert data["ship_json"]["boostCapacitorPercentCost"] == 10.0
    assert data["ship_json"]["boostCapacityPercentChargeRate"] == 200.0
    assert data["ship_json"]["boostMaxSpeedDropOffTime"] == 10.2
    assert data["ship_json"]["boostRechargeTime"] == 20.3
    assert data["ship_json"]["inertiaTensorMultiplier"] == 60


@pytest.mark.asyncio
async def test_get_ship_by_name(async_client: AsyncClient) -> None:
    await async_client.post("/auth/register", json=user_payload)

    response = await async_client.post("/auth/jwt/login", data=form_data)
    data = response.json()

    token = data["access_token"]

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    await async_client.post("/ships/", headers=headers, json=ship_payload)

    response = await async_client.get("/ships/name/Test Ship")
    data = response.json()

    assert response.status_code == status.HTTP_200_OK

    assert data["description"] == "Test description"
    assert data["name"] == "Test Ship"
    assert data["ship_json"]["angularDrag"] == 10.0
    assert data["ship_json"]["boostCapacitorPercentCost"] == 10.0
    assert data["ship_json"]["boostCapacityPercentChargeRate"] == 200.0
    assert data["ship_json"]["boostMaxSpeedDropOffTime"] == 10.2
    assert data["ship_json"]["boostRechargeTime"] == 20.3
    assert data["ship_json"]["inertiaTensorMultiplier"] == 60


@pytest.mark.asyncio
async def test_delete_ship_by_id(async_client: AsyncClient) -> None:
    await async_client.post("/auth/register", json=user_payload)

    response = await async_client.post("/auth/jwt/login", data=form_data)
    data = response.json()

    token = data["access_token"]

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    await async_client.post("/ships/", headers=headers, json=ship_payload)

    response = await async_client.delete("/ships/id/1", headers=headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.asyncio
async def test_rating_ship_by_id(async_client: AsyncClient) -> None:
    await async_client.post("/auth/register", json=user_payload)

    response = await async_client.post("/auth/jwt/login", data=form_data)
    data = response.json()

    token = data["access_token"]

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    await async_client.post("/ships/", headers=headers, json=ship_payload)

    response = await async_client.put("/ships/1/rating/1", headers=headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = await async_client.put("/ships/1/rating/0", headers=headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT
