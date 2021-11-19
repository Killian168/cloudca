from pydantic import BaseModel
from typing import List


class Manager(BaseModel):
    """ Represents what a manager is in the club.
        Holds custom attributes that are related to a Manger role in the Club.
    """
    teams: List[str]
    favorite_formation: str
    training_times: List[str]
    win_record: int
    loss_record: int
    training_times: List[str]
    match_times: List[str]
    achievements: List[str]
