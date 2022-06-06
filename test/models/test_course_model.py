from sqlalchemy.exc import IntegrityError

from database.models.models import User, Course
import pytest
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_course_create_model_with_attached_user(session: AsyncSession) -> None:
    user = User(email="model_test@example.com", hashed_password="mockhashedpass", username="Model Test")

    session.add(user)
    await session.commit()
    await session.refresh(user)

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

    course = Course(name="Test Course", author_id=user.id, description="Test description", game_type="Free Roam", difficulty="Easy", length="Short", course_json=course_data)

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


@pytest.mark.asyncio
async def test_course_create_model_without_user(session: AsyncSession) -> None:
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

    course = Course(name="Test Course", description="Test description", game_type="Free Roam", difficulty="Easy", length="Short", course_json=course_data)

    session.add(course)
    await session.commit()
    await session.refresh(course)

    assert course.id
    assert course.name == "Test Course"
    assert course.author_id is None
    assert course.description == "Test description"
    assert course.game_type == "Free Roam"
    assert course.difficulty == "Easy"
    assert course.length == "Short"
    assert course.course_json == course_data


@pytest.mark.asyncio
async def test_course_create_model_with_attached_user_then_delete_user(session: AsyncSession) -> None:
    user = User(email="model_test@example.com", hashed_password="mockhashedpass", username="Model Test")

    session.add(user)
    await session.commit()
    await session.refresh(user)

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

    await session.delete(user)
    await session.commit()
    await session.refresh(course)

    assert course.id
    assert course.name == "Test Course"
    assert course.author_id is None
    assert course.description == "Test description"
    assert course.game_type == "Free Roam"
    assert course.difficulty == "Easy"
    assert course.length == "Short"
    assert course.course_json == course_data



@pytest.mark.asyncio
async def test_fail_course_create_model_on_duplicate_name(session: AsyncSession) -> None:
    with pytest.raises(IntegrityError):
        user = User(email="model_test@example.com", hashed_password="mockhashedpass", username="Model Test")

        session.add(user)
        await session.commit()
        await session.refresh(user)

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

        course = Course(name="Test Course", author_id=user.id, description="Test description", game_type="Free Roam", difficulty="Easy", length="Short", course_json=course_data)

        session.add(course)
        await session.commit()
        await session.refresh(course)

        course1 = Course(name="Test Course", author_id=user.id, description="Test description", game_type="Free Roam",
                        difficulty="Easy", length="Short", course_json=course_data)

        session.add(course1)
        await session.commit()
