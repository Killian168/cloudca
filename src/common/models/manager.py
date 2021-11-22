from typing import List

from pydantic import BaseModel


class Manager(BaseModel):
    """Represents what a manager is in the club.
    Holds custom attributes that are related to a Manger role in the Club.
    """

    favorite_formation: str
    win_record: int
    loss_record: int
    achievements: List[str]
