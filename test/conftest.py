import asyncio
from typing import AsyncGenerator, Generator, Callable
from unittest import mock

import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import Base, async_session_maker, engine

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()


@pytest_asyncio.fixture(scope="session")
def event_loop(request) -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def session() -> AsyncSession:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
        async with async_session_maker(bind=connection) as session:
            yield session
            await session.flush()
            await session.rollback()


@pytest_asyncio.fixture
def override_get_async_session(session: AsyncSession) -> Callable:
    async def _override_get_async_session():
        yield session

    return _override_get_async_session


@pytest_asyncio.fixture
def app(override_get_async_session: Callable) -> FastAPI:
    from database.database import get_async_session
    from main import app

    app.dependency_overrides[get_async_session] = override_get_async_session
    return app


@pytest_asyncio.fixture
async def async_client(app: FastAPI) -> AsyncGenerator:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
