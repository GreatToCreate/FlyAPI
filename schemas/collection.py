from typing import Optional
from pydantic import BaseModel, validator
from uuid import UUID
from .course import CourseRead


class Collection(BaseModel):
    """
    Collections are user-made course playlists that contain 0 course members at creation
    """
    description: str


class CollectionIn(Collection):
    """
    Schema used for creating a new Collection. Currently this is just name and description from above,
    but this provides flexibility in case future changes require parameters that are only needed at creation time
    """
    name: str


class CollectionUpdate(Collection):
    pass


class CollectionRead(Collection):
    """
    Schema used when returning a Collection object. Inherits all of Collection with the additional attributes listed
    within this class
    """
    id: int
    name: str
    author_id: UUID
    courses: Optional[list[CourseRead]]

    # This validator produces an empty list on read in a scenario where it doesn't exist and otherwise converts list[
    # models.Course] into list[CourseRead]
    @validator("courses", pre=True, always=True)
    def set_courses(cls, v):
        return [CourseRead(**course.__dict__) for course in v] or []


class CollectionAddCourse(BaseModel):
    """
    Used for populating the associative table, collection_has_course, that requires both the collection and course to
    already exist
    """
    collection_id: int
    course_id: int
