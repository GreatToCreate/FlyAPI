from pydantic import BaseModel
import uuid


class ShipJSON(BaseModel):
    """
    Validation class for the actual Fly Dangerous ship JSON. If changes to the parameters are made on the Fly
    Dangerous, we need to update to add the new parameters here
    """
    angularDrag: float
    boostCapacitorPercentCost: float
    boostCapacityPercentChargeRate: float
    boostMaxSpeedDropOffTime: float
    boostRechargeTime: float
    drag: float
    inertiaTensorMultiplier: float
    latHMultiplier: float
    latVMultiplier: float
    mass: float
    maxAngularVelocity: float
    maxBoostSpeed: float
    maxSpeed: float
    maxThrust: float
    minUserLimitedVelocity: float
    pitchMultiplier: float
    rollMultiplier: float
    throttleMultiplier: float
    thrustBoostMultiplier: float
    torqueBoostMultiplier: float
    torqueThrustMultiplier: float
    totalBoostRotationalTime: float
    totalBoostTime: float
    yawMultiplier: float


class Ship(BaseModel):
    """
    The base Ship schema containing all the shared attributed that are inherited by other Ship schemas
    """
    description: str
    ship_json: ShipJSON


class ShipIn(Ship):
    """
    The Ship schema for Ship creation. Currently, the same as the Ship base schema, but provides flexibility in case
    future revision require attributes only needed at creation
    """
    name: str


class ShipUpdate(Ship):
    pass


class ShipDelete(BaseModel):
    id: int


# ToDo consider adding the author username onto this field
class ShipRead(Ship):
    """
    The Ship schema used for returning information about a particular ship (on get requests)
    """
    id: int
    name: str
    author_id: uuid.UUID
