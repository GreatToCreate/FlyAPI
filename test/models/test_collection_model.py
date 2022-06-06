from sqlalchemy.exc import IntegrityError

from database.models.models import User, Collection
import pytest
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_collection_create_model_with_attached_user(session: AsyncSession) -> None:
    user = User(email="model_test@example.com", hashed_password="mockhashedpass", username="Model Test")

    session.add(user)
    await session.commit()
    await session.refresh(user)

    collection = Collection(name="Test Collection", author_id=user.id, description="Test description")

    session.add(collection)
    await session.commit()
    await session.refresh(collection)

    assert collection.id
    assert collection.name == "Test Collection"
    assert collection.author_id == user.id
    assert collection.description == "Test description"


@pytest.mark.asyncio
async def test_collection_create_model_without_user(session: AsyncSession) -> None:
    collection = Collection(name="Test Collection", description="Test description")

    session.add(collection)
    await session.commit()
    await session.refresh(collection)

    assert collection.id
    assert collection.name == "Test Collection"
    assert collection.description == "Test description"


@pytest.mark.asyncio
async def test_collection_create_model_with_attached_user_then_delete_user(session: AsyncSession) -> None:
    user = User(email="model_test@example.com", hashed_password="mockhashedpass", username="Model Test")

    session.add(user)
    await session.commit()
    await session.refresh(user)

    collection = Collection(name="Test Collection", author_id=user.id, description="Test description")

    session.add(collection)
    await session.commit()
    await session.refresh(collection)

    await session.delete(user)
    await session.commit()
    await session.refresh(collection)

    assert collection.id
    assert collection.name == "Test Collection"
    assert collection.description == "Test description"


@pytest.mark.asyncio
async def test_fail_collection_create_model_on_duplicate_name(session: AsyncSession) -> None:
    with pytest.raises(IntegrityError):
        user = User(email="model_test@example.com", hashed_password="mockhashedpass", username="Model Test")

        session.add(user)
        await session.commit()
        await session.refresh(user)

        collection = Collection(name="Test Collection", author_id=user.id, description="Test description")

        session.add(collection)
        await session.commit()
        await session.refresh(collection)

        collection1 = Collection(name="Test Collection", author_id=user.id, description="Test description")

        session.add(collection1)
        await session.commit()
