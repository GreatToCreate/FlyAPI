import pytest
from httpx import AsyncClient
from starlette import status


@pytest.mark.asyncio
async def test_main(async_client: AsyncClient) -> None:
    response = await async_client.get("/")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Not Found"}
