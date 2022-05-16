from typing import List

import attrs

from ..models.cognito_user import CognitoMember


@attrs.define
class AcademyPlayer:
    """Represents what an academy player is in the club.
    Holds custom attributes that are related to a Academy Player role in the Club.
    """

    allergies: str
    asthma: str
    diabetes: str
    medication: str
    notes: str
    guardians: List[CognitoMember]
