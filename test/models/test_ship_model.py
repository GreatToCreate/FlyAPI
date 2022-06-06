from sqlalchemy.exc import IntegrityError

from database.models.models import User, Ship
import pytest
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_ship_create_model_with_attached_user(session: AsyncSession) -> None:
    user = User(email="model_test@example.com", hashed_password="mockhashedpass", username="Model Test")

    session.add(user)
    await session.commit()
    await session.refresh(user)

    ship_data = {
        "angularDrag": 100.0,
        "boostCapacitorPercentCost": 0,
        "boostCapacityPercentChargeRate": 0,
        "boostMaxSpeedDropOffTime": 0,
        "boostRechargeTime": 0,
        "drag": 0,
        "inertiaTensorMultiplier": 0,
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
        "yawMultiplier": 2
    }

    ship = Ship(name="Test Ship", author_id=user.id, description="Test description", ship_json=ship_data)

    session.add(ship)
    await session.commit()
    await session.refresh(ship)

    assert ship.name == "Test Ship"
    assert ship.author_id == user.id
    assert ship.ship_json == ship_data


@pytest.mark.asyncio
async def test_ship_create_model_without_user(session: AsyncSession) -> None:
    ship_data = {
        "angularDrag": 100.0,
        "boostCapacitorPercentCost": 0,
        "boostCapacityPercentChargeRate": 0,
        "boostMaxSpeedDropOffTime": 0,
        "boostRechargeTime": 0,
        "drag": 0,
        "inertiaTensorMultiplier": 0,
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
        "yawMultiplier": 2
    }

    ship = Ship(name="Test Ship", description="Test description", ship_json=ship_data)

    session.add(ship)
    await session.commit()
    await session.refresh(ship)

    assert ship.name == "Test Ship"
    assert ship.author_id is None
    assert ship.ship_json == ship_data


@pytest.mark.asyncio
async def test_ship_create_model_with_attached_user_then_delete_user(session: AsyncSession) -> None:
    user = User(email="model_test@example.com", hashed_password="mockhashedpass", username="Model Test")

    session.add(user)
    await session.commit()
    await session.refresh(user)

    ship_data = {
        "angularDrag": 100.0,
        "boostCapacitorPercentCost": 0,
        "boostCapacityPercentChargeRate": 0,
        "boostMaxSpeedDropOffTime": 0,
        "boostRechargeTime": 0,
        "drag": 0,
        "inertiaTensorMultiplier": 0,
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
        "yawMultiplier": 2
    }

    ship = Ship(name="Test Ship", author_id=user.id, description="Test description", ship_json=ship_data)

    session.add(ship)
    await session.commit()
    await session.refresh(ship)

    await session.delete(user)
    await session.commit()
    await session.refresh(ship)

    assert ship.name == "Test Ship"
    assert ship.author_id is None
    assert ship.ship_json == ship_data



@pytest.mark.asyncio
async def test_fail_ship_create_model_on_duplicate_name(session: AsyncSession) -> None:
    with pytest.raises(IntegrityError):
        user = User(email="model_test@example.com", hashed_password="mockhashedpass", username="Model Test")

        session.add(user)
        await session.commit()
        await session.refresh(user)

        ship_data = {
            "angularDrag": 100.0,
            "boostCapacitorPercentCost": 0,
            "boostCapacityPercentChargeRate": 0,
            "boostMaxSpeedDropOffTime": 0,
            "boostRechargeTime": 0,
            "drag": 0,
            "inertiaTensorMultiplier": 0,
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
            "yawMultiplier": 2
        }

        ship = Ship(name="Test Ship", author_id=user.id, description="Test description", ship_json=ship_data)

        session.add(ship)
        await session.commit()
        await session.refresh(ship)

        ship1 = Ship(name="Test Ship", author_id=user.id, description="Test description", ship_json=ship_data)

        session.add(ship1)
        await session.commit()
