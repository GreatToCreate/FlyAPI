from typing import Optional
from enum import Enum

from pydantic import BaseModel
from uuid import UUID


class Coordinate3D(BaseModel):
    """
    Base class for any node requiring a floating point 3d vector
    """
    x: float
    y: float
    z: float


class Position(Coordinate3D):
    """
    An arbitrary point in 3d space defined by its x,y,z coordinates
    """
    pass


# ToDo better document what Rotation actually means in an xyz coordinate system
class Rotation(Coordinate3D):
    """

    """
    pass


# ToDo explain what these types actually represent [Find them in Fly Dangerous codebase]
class CheckpointTypeEnum(Enum):
    """

    """
    zero = 0
    one = 1
    two = 2


class Checkpoint(BaseModel):
    """
    The defined position, rotation, and type of a checkpoint to be used the checkpoints list within the course_json
    """
    position: Position
    rotation: Rotation
    type: CheckpointTypeEnum

    class Config:
        use_enum_values = True


# ToDo Better understanding of what x,y,z gravity represents
class Gravity(Coordinate3D):
    pass


class StartPosition(Coordinate3D):
    """
    The 3 x,y,z coordinates that determine the ship's starting location on custom map load
    """
    pass


class StartRotation(Coordinate3D):
    """
    The 3 x,y,z, coordinates that determine the ships starting rotation on custom map load
    """
    pass


class LocationEnum(Enum):
    """
    The map archetypes available to create a custom map
    """
    space = "Space"
    space_station = "Space Station"
    flat_world = "Flat World"
    canyons = "Canyons"
    biome_world = "Biome World"


class EnvironmentEnum(Enum):
    """
    The environmental archetypes available to create a custom map
    """
    none_selected = ""
    sunrise_clear = "Sunrise Clear"
    noon_clear = "Noon Clear"
    noon_cloudy = "Noon Cloudy"
    noon_stormy = "Noon Stormy"
    sunset_clear = "Sunset Clear"
    sunset_cloudy = "Sunset Cloudy"
    night_clear = "Night Clear"
    night_cloudy = "Night Cloudy"
    red_planet = "Red Planet"
    blue_planet = "Blue Planet"
    red_blue_nebula = "Red / Blue Nebula",
    yellow_green_nebula = "Yellow / Green Nebula"


class GameTypeEnum(Enum):
    """
    The gametype archetypes available to set the style of gameplay in a custom map
    """
    free_roam = "Free Roam"
    time_trial = "Time Trial"
    sprint = "Sprint"
    laps = "Laps"
    hoon_attack = "Hoon Attack"
    training = "Training"


class VersionEnum(Enum):
    """
    The versioning scheme for the custom track JSON definition of Fly Dangerous
    """
    one = 1


class MusicTrackEnum(Enum):
    """
    The music archetypes available to set the audio track to play in a custom map
    """
    none_selected = ""
    juno = "Juno"
    beautiful_catastrophe = "Beautiful Catastrophe"
    digital_battleground = "Digital Battleground"
    chaos_at_the_spaceship = "Chaos at the Spaceship"
    hydra = "Hydra"
    hooligans = "Hooligans"


class CourseJSON(BaseModel):
    """
    A PyDantic model used to validate the structure of a given custom track JSON
    """
    version: VersionEnum
    name: str
    location: LocationEnum
    environment: EnvironmentEnum
    terrainSeed: str
    gravity: Gravity
    startPosition: StartPosition
    startRotation: StartRotation
    gameType: GameTypeEnum
    musicTrack: MusicTrackEnum
    authorTimeTarget: Optional[float]
    checkpoints: list[Checkpoint]

    class Config:
        use_enum_values = True


class DifficultyEnum(Enum):
    """
    The difficulty metadata archetypes available for defining how hard a course is. Not a Fly Dangerous JSON attribute
    """
    easy = "Easy"
    medium = "Medium"
    hard = "Hard"
    dangerous = "Dangerous"


class LengthEnum(Enum):
    """
    The length metadata archetypes available for defining how long a course is. Not a Fly Dangerous JSON attribute
    """
    short = "Short"
    medium = "Medium"
    long = "Long"
    endurance = "Endurance"


class Course(BaseModel):
    """
    The base Course schema containing the attributes that all other Course-related schemas will inherit
    """
    description: str
    # Possible future functionality on the Fly Dangerous side of things
    # ship_json: dict
    game_type: GameTypeEnum
    difficulty: DifficultyEnum
    length: LengthEnum
    course_json: CourseJSON
    # Potential model change required to support this. Do people care about location filtering?
    # location: str

    class Config:
        use_enum_values = True


class CourseUpdate(Course):
    link: Optional[str]


class CourseIn(Course):
    """
    The Course schema used for validation to ensure that all fields are correctly set/defined before being persisted
    as a course database entry
    """
    name: str
    link: Optional[str]


# ToDo define collection in Pydantic schema so that I can have it optionally sitting on the CourseRead schema
#  def Debating whether I want this functionality available now. It's cool to see how many collections a course is
#  in, but is it really useful?
class CourseRead(Course):
    id: int
    name: str
    author_id: UUID
