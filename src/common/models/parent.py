from pydantic import BaseModel

from ..models.cognito_user import CognitoMember


class Parent(BaseModel):
    """Represents what a parent is in the club.
    Holds custom attributes that are related to a Parent role in the Club.
    """

    attributes: CognitoMember
