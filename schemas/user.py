import uuid

from fastapi_users import schemas


# ToDo Does this need augmentation with the extensions to the base User model? E.G. username, steam_id, steam_username
class UserRead(schemas.BaseUser[uuid.UUID]):
    """
    The Fastapi-Users base model for a User
    """
    pass


class UserCreate(schemas.BaseUserCreate):
    username: str


class UserUpdate(schemas.BaseUserUpdate):
    pass
