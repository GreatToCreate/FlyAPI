from typing import Optional

from pydantic import BaseModel


class Leader(BaseModel):
    """
    Base class for a leader entry
    """
    steam_username: Optional[str]
    steam_id: Optional[int]
    points: int

    class Config:
        orm_mode = True


class TopScore(BaseModel):
    """
    Base class for a top score entry
    """
    course: str
    steam_id: int
    steam_username: Optional[str]
    time: Optional[int]
    points: int

    class Config:
        orm_mode = True
