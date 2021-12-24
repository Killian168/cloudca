from typing import List, Optional
from uuid import uuid4

from pydantic import BaseModel, validator

from ..models.fixture import Fixture


class Team(BaseModel):
    """Represents what a team is in the club.
    Holds custom attributes that are related to a Team in the Club.
    """

    id: Optional[str]
    name: str
    managers: List[str] = []
    players: List[str] = []
    training_times: List[str] = []
    fixtures: List[Fixture] = []

    @validator("id", always=True)
    def check_member_has_id(cls, value):
        return value or str(uuid4())
