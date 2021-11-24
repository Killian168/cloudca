from typing import List

from pydantic import BaseModel

from ..models.cognito_user import CognitoMember


class AcademyPlayer(BaseModel):
    """Represents what an academy player is in the club.
    Holds custom attributes that are related to a Academy Player role in the Club.
    """

    allergies: str
    asthma: str
    diabetes: str
    medication: str
    notes: str
    guardians: List[CognitoMember]
