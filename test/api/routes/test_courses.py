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

course_payload = {
    "description": "Slippery Snake from custom-races discord",
    "game_type": "Time Trial",
    "difficulty": "Hard",
    "length": "Short",
    "course_json": {
        "authorTimeTarget": 0.0,
        "checkpoints": [
            {
                "position": {
                    "x": 100000.0,
                    "y": 100000.0,
                    "z": 99692.0
                },
                "rotation": {
                    "x": 0.0,
                    "y": 0.0,
                    "z": 0.0
                },
                "type": 0
            },
            {
                "position": {
                    "x": 99037.22,
                    "y": 100456.281,
                    "z": 102098.844
                },
                "rotation": {
                    "x": 357.0515,
                    "y": 11.5882988,
                    "z": 359.3957
                },
                "type": 1
            },
            {
                "position": {
                    "x": 99198.0,
                    "y": 100529.0,
                    "z": 103482.0
                },
                "rotation": {
                    "x": 338.087067,
                    "y": 69.39353,
                    "z": 352.435974
                },
                "type": 1
            },
            {
                "position": {
                    "x": 100292.0,
                    "y": 101935.0,
                    "z": 103409.0
                },
                "rotation": {
                    "x": 330.8563,
                    "y": 139.335022,
                    "z": 11.77235
                },
                "type": 1
            },
            {
                "position": {
                    "x": 101835.0,
                    "y": 102244.0,
                    "z": 100669.0
                },
                "rotation": {
                    "x": 72.920105,
                    "y": 263.533234,
                    "z": 210.6785
                },
                "type": 1
            },
            {
                "position": {
                    "x": 99568.0,
                    "y": 103851.0,
                    "z": 99185.0
                },
                "rotation": {
                    "x": 12.73269,
                    "y": 52.62485,
                    "z": 354.5677
                },
                "type": 1
            },
            {
                "position": {
                    "x": 97640.0,
                    "y": 103790.0,
                    "z": 98015.0
                },
                "rotation": {
                    "x": 344.313568,
                    "y": 87.19779,
                    "z": 349.291168
                },
                "type": 1
            },
            {
                "position": {
                    "x": 96520.0,
                    "y": 98983.0,
                    "z": 100113.0
                },
                "rotation": {
                    "x": 316.76178,
                    "y": 61.0900459,
                    "z": 356.469147
                },
                "type": 1
            },
            {
                "position": {
                    "x": 91058.0,
                    "y": 98308.0,
                    "z": 99014.0
                },
                "rotation": {
                    "x": 18.76304,
                    "y": 70.69238,
                    "z": 356.977936
                },
                "type": 1
            },
            {
                "position": {
                    "x": 100821.0,
                    "y": 104342.0,
                    "z": 100262.0
                },
                "rotation": {
                    "x": 70.69469,
                    "y": 37.8761024,
                    "z": 342.5133
                },
                "type": 1
            },
            {
                "position": {
                    "x": 90163.0,
                    "y": 99684.0,
                    "z": 98768.0
                },
                "rotation": {
                    "x": 65.10054,
                    "y": 58.2459068,
                    "z": 338.847748
                },
                "type": 2
            },
            {
                "position": {
                    "x": 98621.0,
                    "y": 103623.0,
                    "z": 98563.0
                },
                "rotation": {
                    "x": 274.785,
                    "y": 343.197968,
                    "z": 86.2812042
                },
                "type": 1
            },
            {
                "position": {
                    "x": 96351.0,
                    "y": 103309.0,
                    "z": 97551.0
                },
                "rotation": {
                    "x": 334.4366,
                    "y": 157.994751,
                    "z": 301.600769
                },
                "type": 1
            },
            {
                "position": {
                    "x": 101302.0,
                    "y": 103594.0,
                    "z": 102496.0
                },
                "rotation": {
                    "x": 70.69469,
                    "y": 37.8761024,
                    "z": 342.5133
                },
                "type": 1
            },
            {
                "position": {
                    "x": 96446.0,
                    "y": 102561.0,
                    "z": 99763.0
                },
                "rotation": {
                    "x": 64.24008,
                    "y": 0.0,
                    "z": 0.0
                },
                "type": 1
            },
            {
                "position": {
                    "x": 96936.0,
                    "y": 99897.0,
                    "z": 101245.0
                },
                "rotation": {
                    "x": 90.0,
                    "y": 0.0,
                    "z": 0.0
                },
                "type": 1
            },
            {
                "position": {
                    "x": 96936.0,
                    "y": 100883.0,
                    "z": 100818.0
                },
                "rotation": {
                    "x": 90.0,
                    "y": 0.0,
                    "z": 0.0
                },
                "type": 1
            },
            {
                "position": {
                    "x": 96936.0,
                    "y": 101724.0,
                    "z": 100463.0
                },
                "rotation": {
                    "x": 90.0,
                    "y": 0.0,
                    "z": 0.0
                },
                "type": 1
            },
            {
                "position": {
                    "x": 94653.0,
                    "y": 98652.0,
                    "z": 98797.0
                },
                "rotation": {
                    "x": 353.803467,
                    "y": 84.52866,
                    "z": 355.752228
                },
                "type": 1
            },
            {
                "position": {
                    "x": 95660.0,
                    "y": 99118.0,
                    "z": 98697.0
                },
                "rotation": {
                    "x": 354.893555,
                    "y": 50.7631836,
                    "z": 11.5420313
                },
                "type": 1
            }
        ],
        "environment": "Red / Blue Nebula",
        "gameType": "Time Trial",
        "gravity": {
            "x": 0.0,
            "y": 0.0,
            "z": 0.0
        },
        "location": "Space",
        "musicTrack": "",
        "name": "Slippery Snake",
        "startPosition": {
            "x": 100000.0,
            "y": 100000.0,
            "z": 99692.0
        },
        "startRotation": {
            "x": 0.0,
            "y": 0.0,
            "z": 0.0
        },
        "terrainSeed": "",
        "version": 1
    },
    "name": "Slippery Snake",
    "link": "string"
}

form_data = {
        "username": "test@example.com",
        "password": "test"
}


@pytest.mark.asyncio
async def test_create_course(async_client: AsyncClient) -> None:
    await async_client.post("/auth/register", json=user_payload)

    response = await async_client.post("/auth/jwt/login", data=form_data)
    data = response.json()

    token = data["access_token"]

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = await async_client.post("/courses/", headers=headers, json=course_payload)
    data = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert data["description"] == "Slippery Snake from custom-races discord"
    assert data["name"] == "Slippery Snake"
    assert data["course_json"] == course_payload["course_json"]
    assert data["game_type"] == "Time Trial"
    assert data["difficulty"] == "Hard"
    assert data["length"] == "Short"


@pytest.mark.asyncio
async def test_get_courses(async_client: AsyncClient) -> None:
    await async_client.post("/auth/register", json=user_payload)

    response = await async_client.post("/auth/jwt/login", data=form_data)
    data = response.json()

    token = data["access_token"]

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }


    await async_client.post("/courses/", headers=headers, json=course_payload)

    response = await async_client.get("/courses/")
    data = response.json()

    assert len(data) == 1

    assert response.status_code == status.HTTP_200_OK

    assert data[0]["description"] == "Slippery Snake from custom-races discord"
    assert data[0]["name"] == "Slippery Snake"
    assert data[0]["game_type"] == "Time Trial"
    assert data[0]["difficulty"] == "Hard"
    assert data[0]["length"] == "Short"


@pytest.mark.asyncio
async def test_get_course_by_id(async_client: AsyncClient) -> None:
    await async_client.post("/auth/register", json=user_payload)

    response = await async_client.post("/auth/jwt/login", data=form_data)
    data = response.json()

    token = data["access_token"]

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    await async_client.post("/courses/", headers=headers, json=course_payload)

    response = await async_client.get("/courses/id/1")
    data = response.json()

    assert response.status_code == status.HTTP_200_OK

    assert data["description"] == "Slippery Snake from custom-races discord"
    assert data["name"] == "Slippery Snake"
    assert data["game_type"] == "Time Trial"
    assert data["difficulty"] == "Hard"
    assert data["length"] == "Short"


@pytest.mark.asyncio
async def test_get_course_by_name(async_client: AsyncClient) -> None:
    await async_client.post("/auth/register", json=user_payload)

    response = await async_client.post("/auth/jwt/login", data=form_data)
    data = response.json()

    token = data["access_token"]

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    await async_client.post("/courses/", headers=headers, json=course_payload)

    response = await async_client.get("/courses/name/Slippery Snake")
    data = response.json()

    assert response.status_code == status.HTTP_200_OK

    assert data["description"] == "Slippery Snake from custom-races discord"
    assert data["name"] == "Slippery Snake"
    assert data["game_type"] == "Time Trial"
    assert data["difficulty"] == "Hard"
    assert data["length"] == "Short"


@pytest.mark.asyncio
async def test_delete_course_by_id(async_client: AsyncClient) -> None:
    await async_client.post("/auth/register", json=user_payload)

    response = await async_client.post("/auth/jwt/login", data=form_data)
    data = response.json()

    token = data["access_token"]

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    await async_client.post("/courses/", headers=headers, json=course_payload)
    response = await async_client.delete("/courses/id/1", headers=headers)

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.asyncio
async def test_rating_course_by_id(async_client: AsyncClient) -> None:
    await async_client.post("/auth/register", json=user_payload)

    response = await async_client.post("/auth/jwt/login", data=form_data)
    data = response.json()

    token = data["access_token"]

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    await async_client.post("/courses/", headers=headers, json=course_payload)

    response = await async_client.put("/courses/1/rating/1", headers=headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = await async_client.put("/courses/1/rating/0", headers=headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT
