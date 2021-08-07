from pydantic import BaseModel
from ..models.parent import Parent
from typing import List


class AcademyPlayer(BaseModel):
    """ Represents what an academy player is in the club.
        Holds custom attributes that are related to a Academy Player role in the Club.
    """
    allergies: str
    asthma: str
    diabetes: str
    medication: str
    notes: str
    parents: List[Parent]
