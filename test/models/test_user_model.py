from sqlalchemy.exc import IntegrityError

from database.models.models import User
import pytest
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_user_create_model(session: AsyncSession) -> None:
    user = User(email="model_test@example.com", hashed_password="mockhashedpass", username="Model Test")

    session.add(user)
    await session.commit()
    await session.refresh(user)

    assert user.email == "model_test@example.com"
    assert user.hashed_password == "mockhashedpass"
    assert user.username == "Model Test"


@pytest.mark.asyncio
async def test_fail_user_create_model_on_duplicate_email_and_username(session: AsyncSession) -> None:
    with pytest.raises(IntegrityError):
        user = User(email="model_test@example.com", hashed_password="mockhashedpass", username="Model Test")

        session.add(user)
        await session.commit()
        await session.refresh(user)

        user1 = User(email="model_test@example.com", hashed_password="mockhashedpass", username="Model Test")

        session.add(user1)
        await session.commit()


@pytest.mark.asyncio
async def test_fail_user_create_model_on_duplicate_email(session: AsyncSession) -> None:
    with pytest.raises(IntegrityError):
        user = User(email="model_test@example.com", hashed_password="mockhashedpass", username="Model Test 1")

        session.add(user)
        await session.commit()
        await session.refresh(user)

        user1 = User(email="model_test@example.com", hashed_password="mockhashedpass", username="Model Test 2")

        session.add(user1)
        await session.commit()


@pytest.mark.asyncio
async def test_fail_user_create_model_on_duplicate_username(session: AsyncSession) -> None:
    with pytest.raises(IntegrityError):
        user = User(email="model_test1@example.com", hashed_password="mockhashedpass", username="Model Test")

        session.add(user)
        await session.commit()
        await session.refresh(user)

        user1 = User(email="model_test2@example.com", hashed_password="mockhashedpass", username="Model Test")

        session.add(user1)
        await session.commit()







