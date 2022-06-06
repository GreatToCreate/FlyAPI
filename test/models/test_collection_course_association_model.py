from database.models.models import User, Course, Collection
import pytest
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_collection_and_course_create_add_course_to_collection_associative_model_with_attached_user(
        session: AsyncSession) -> None:
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

    course_data = {
        "version": 1,
        "name": "string",
        "location": "Space",
        "environment": "Sunrise Clear",
        "terrainSeed": "",
        "gravity": {
            "x": 0,
            "y": 0,
            "z": 0
        },
        "startPosition": {
            "x": 0,
            "y": 0,
            "z": 0
        },
        "startRotation": {
            "x": 0,
            "y": 0,
            "z": 0
        },
        "gameType": "Free Roam",
        "musicTrack": "Juno",
        "authorTimeTarget": 0,
        "checkpoints": [
            {
                "position": {
                    "x": 0,
                    "y": 0,
                    "z": 0
                },
                "rotation": {
                    "x": 0,
                    "y": 0,
                    "z": 0
                },
                "type": 1
            }
        ]
    }

    course = Course(name="Test Course", author_id=user.id, description="Test description", game_type="Free Roam",
                    difficulty="Easy", length="Short", course_json=course_data)

    session.add(course)
    await session.commit()
    await session.refresh(course)

    assert course.id
    assert course.name == "Test Course"
    assert course.author_id == user.id
    assert course.description == "Test description"
    assert course.game_type == "Free Roam"
    assert course.difficulty == "Easy"
    assert course.length == "Short"
    assert course.course_json == course_data

    collection.courses.append(course)
    await session.commit()
    await session.refresh(collection)
    await session.refresh(course)

    associative_table_result = await session.execute("""SELECT collection_id, course_id FROM collection_has_course""")
    associative_table = associative_table_result.first()

    assert associative_table == (collection.id, course.id)
    assert collection.courses[0].__dict__ == course.__dict__


@pytest.mark.asyncio
async def test_collection_and_course_create_add_course_to_collection_associative_model_without_user(
        session: AsyncSession) -> None:
    collection = Collection(name="Test Collection", description="Test description")

    session.add(collection)
    await session.commit()
    await session.refresh(collection)

    course_data = {
        "version": 1,
        "name": "string",
        "location": "Space",
        "environment": "Sunrise Clear",
        "terrainSeed": "",
        "gravity": {
            "x": 0,
            "y": 0,
            "z": 0
        },
        "startPosition": {
            "x": 0,
            "y": 0,
            "z": 0
        },
        "startRotation": {
            "x": 0,
            "y": 0,
            "z": 0
        },
        "gameType": "Free Roam",
        "musicTrack": "Juno",
        "authorTimeTarget": 0,
        "checkpoints": [
            {
                "position": {
                    "x": 0,
                    "y": 0,
                    "z": 0
                },
                "rotation": {
                    "x": 0,
                    "y": 0,
                    "z": 0
                },
                "type": 1
            }
        ]
    }

    course = Course(name="Test Course", description="Test description", game_type="Free Roam",
                    difficulty="Easy", length="Short", course_json=course_data)

    session.add(course)
    await session.commit()
    await session.refresh(course)

    collection.courses.append(course)
    await session.commit()
    await session.refresh(collection)
    await session.refresh(course)

    associative_table_result = await session.execute("""SELECT collection_id, course_id FROM collection_has_course""")
    associative_table = associative_table_result.first()

    assert associative_table == (collection.id, course.id)
    assert collection.courses[0].__dict__ == course.__dict__


@pytest.mark.asyncio
async def test_collection_and_course_create_add_course_to_collection_associative_model_with_attached_user_then_del_user(
        session: AsyncSession) -> None:
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

    course_data = {
        "version": 1,
        "name": "string",
        "location": "Space",
        "environment": "Sunrise Clear",
        "terrainSeed": "",
        "gravity": {
            "x": 0,
            "y": 0,
            "z": 0
        },
        "startPosition": {
            "x": 0,
            "y": 0,
            "z": 0
        },
        "startRotation": {
            "x": 0,
            "y": 0,
            "z": 0
        },
        "gameType": "Free Roam",
        "musicTrack": "Juno",
        "authorTimeTarget": 0,
        "checkpoints": [
            {
                "position": {
                    "x": 0,
                    "y": 0,
                    "z": 0
                },
                "rotation": {
                    "x": 0,
                    "y": 0,
                    "z": 0
                },
                "type": 1
            }
        ]
    }

    course = Course(name="Test Course", author_id=user.id, description="Test description", game_type="Free Roam",
                    difficulty="Easy", length="Short", course_json=course_data)

    session.add(course)
    await session.commit()
    await session.refresh(course)

    assert course.id
    assert course.name == "Test Course"
    assert course.author_id == user.id
    assert course.description == "Test description"
    assert course.game_type == "Free Roam"
    assert course.difficulty == "Easy"
    assert course.length == "Short"
    assert course.course_json == course_data

    collection.courses.append(course)
    await session.commit()
    await session.refresh(collection)
    await session.refresh(course)

    # Only difference here from the first, removing the user and making sure that this doesn't impact the existing
    # collection
    await session.delete(user)
    await session.commit()
    await session.refresh(collection)
    await session.refresh(course)

    associative_table_result = await session.execute("""SELECT collection_id, course_id FROM collection_has_course""")
    associative_table = associative_table_result.first()

    assert associative_table == (collection.id, course.id)
    assert collection.courses[0].__dict__ == course.__dict__


@pytest.mark.asyncio
async def test_collection_and_course_create_add_course_to_collection_associative_model_with_attached_user_then_del_cour(
        session: AsyncSession) -> None:
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

    course_data = {
        "version": 1,
        "name": "string",
        "location": "Space",
        "environment": "Sunrise Clear",
        "terrainSeed": "",
        "gravity": {
            "x": 0,
            "y": 0,
            "z": 0
        },
        "startPosition": {
            "x": 0,
            "y": 0,
            "z": 0
        },
        "startRotation": {
            "x": 0,
            "y": 0,
            "z": 0
        },
        "gameType": "Free Roam",
        "musicTrack": "Juno",
        "authorTimeTarget": 0,
        "checkpoints": [
            {
                "position": {
                    "x": 0,
                    "y": 0,
                    "z": 0
                },
                "rotation": {
                    "x": 0,
                    "y": 0,
                    "z": 0
                },
                "type": 1
            }
        ]
    }

    course = Course(name="Test Course", author_id=user.id, description="Test description", game_type="Free Roam",
                    difficulty="Easy", length="Short", course_json=course_data)

    session.add(course)
    await session.commit()
    await session.refresh(course)

    collection.courses.append(course)
    await session.commit()
    await session.refresh(collection)
    await session.refresh(course)

    # Only difference here from the first, removing the user and making sure that this doesn't impact the existing
    # collection
    await session.delete(collection)
    await session.commit()
    await session.refresh(course)

    assert course.id
    assert course.name == "Test Course"
    assert course.author_id == user.id
    assert course.description == "Test description"
    assert course.game_type == "Free Roam"
    assert course.difficulty == "Easy"
    assert course.length == "Short"
    assert course.course_json == course_data


@pytest.mark.asyncio
async def test_collection_and_course_create_add_course_to_collection_associative_model_with_attached_user_then_del_coll(
        session: AsyncSession) -> None:
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

    course_data = {
        "version": 1,
        "name": "string",
        "location": "Space",
        "environment": "Sunrise Clear",
        "terrainSeed": "",
        "gravity": {
            "x": 0,
            "y": 0,
            "z": 0
        },
        "startPosition": {
            "x": 0,
            "y": 0,
            "z": 0
        },
        "startRotation": {
            "x": 0,
            "y": 0,
            "z": 0
        },
        "gameType": "Free Roam",
        "musicTrack": "Juno",
        "authorTimeTarget": 0,
        "checkpoints": [
            {
                "position": {
                    "x": 0,
                    "y": 0,
                    "z": 0
                },
                "rotation": {
                    "x": 0,
                    "y": 0,
                    "z": 0
                },
                "type": 1
            }
        ]
    }

    course = Course(name="Test Course", author_id=user.id, description="Test description", game_type="Free Roam",
                    difficulty="Easy", length="Short", course_json=course_data)

    session.add(course)
    await session.commit()
    await session.refresh(course)

    collection.courses.append(course)
    await session.commit()
    await session.refresh(collection)
    await session.refresh(course)

    # Only difference here from the first, removing the user and making sure that this doesn't impact the existing
    # collection
    await session.delete(collection)
    await session.commit()
    await session.refresh(course)

    assert course.id
    assert course.name == "Test Course"
    assert course.author_id == user.id
    assert course.description == "Test description"
    assert course.game_type == "Free Roam"
    assert course.difficulty == "Easy"
    assert course.length == "Short"
    assert course.course_json == course_data


@pytest.mark.asyncio
async def test_collection_and_course_create_add_course_to_collection_associative_model_with_attached_user_then_del_cour(
        session: AsyncSession) -> None:
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

    course_data = {
        "version": 1,
        "name": "string",
        "location": "Space",
        "environment": "Sunrise Clear",
        "terrainSeed": "",
        "gravity": {
            "x": 0,
            "y": 0,
            "z": 0
        },
        "startPosition": {
            "x": 0,
            "y": 0,
            "z": 0
        },
        "startRotation": {
            "x": 0,
            "y": 0,
            "z": 0
        },
        "gameType": "Free Roam",
        "musicTrack": "Juno",
        "authorTimeTarget": 0,
        "checkpoints": [
            {
                "position": {
                    "x": 0,
                    "y": 0,
                    "z": 0
                },
                "rotation": {
                    "x": 0,
                    "y": 0,
                    "z": 0
                },
                "type": 1
            }
        ]
    }

    course = Course(name="Test Course", author_id=user.id, description="Test description", game_type="Free Roam",
                    difficulty="Easy", length="Short", course_json=course_data)

    session.add(course)
    await session.commit()
    await session.refresh(course)

    collection.courses.append(course)
    await session.commit()
    await session.refresh(collection)
    await session.refresh(course)

    await session.delete(course)
    await session.commit()
    await session.refresh(collection)

    assert len(collection.courses) == 0


@pytest.mark.asyncio
async def test_collection_and_course_create_add_course_to_collection_associative_model_with_attached_user_then_rem_cour(
        session: AsyncSession) -> None:
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

    course_data = {
        "version": 1,
        "name": "string",
        "location": "Space",
        "environment": "Sunrise Clear",
        "terrainSeed": "",
        "gravity": {
            "x": 0,
            "y": 0,
            "z": 0
        },
        "startPosition": {
            "x": 0,
            "y": 0,
            "z": 0
        },
        "startRotation": {
            "x": 0,
            "y": 0,
            "z": 0
        },
        "gameType": "Free Roam",
        "musicTrack": "Juno",
        "authorTimeTarget": 0,
        "checkpoints": [
            {
                "position": {
                    "x": 0,
                    "y": 0,
                    "z": 0
                },
                "rotation": {
                    "x": 0,
                    "y": 0,
                    "z": 0
                },
                "type": 1
            }
        ]
    }

    course = Course(name="Test Course", author_id=user.id, description="Test description", game_type="Free Roam",
                    difficulty="Easy", length="Short", course_json=course_data)

    session.add(course)
    await session.commit()
    await session.refresh(course)

    collection.courses.append(course)
    await session.commit()
    await session.refresh(collection)
    await session.refresh(course)

    collection.courses.remove(course)
    await session.commit()
    await session.refresh(collection)
    await session.refresh(course)

    assert course.id
    assert course.name == "Test Course"
    assert course.author_id == user.id
    assert course.description == "Test description"
    assert course.game_type == "Free Roam"
    assert course.difficulty == "Easy"
    assert course.length == "Short"
    assert len(collection.courses) == 0
