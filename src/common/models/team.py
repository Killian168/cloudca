from typing import List

from pydantic import BaseModel

from ..models.fixture import Fixture


class Team(BaseModel):
    """Represents what a team is in the club.
    Holds custom attributes that are related to a Team in the Club.
    """

    id: str
    name: str
    managers: List[str] = []
    players: List[str] = []
    training_times: List[str] = []
    fixtures: List[Fixture] = []
