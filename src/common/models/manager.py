from typing import List

from pydantic import BaseModel


class Manager(BaseModel):
    """Represents what a manager is in the club.
    Holds custom attributes that are related to a Manger role in the Club.
    """

    teams: List[str]
    favorite_formation: str
    training_times: List[str]
    win_record: int
    loss_record: int
    match_times: List[str]
    achievements: List[str]
