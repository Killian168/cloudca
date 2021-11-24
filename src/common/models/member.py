from typing import Optional

from pydantic import BaseModel, root_validator

from ..models.academy_player import AcademyPlayer
from ..models.cognito_user import CognitoMember
from ..models.manager import Manager
from ..models.officer import Officer
from ..models.player import Player


class NoMemberRole(Exception):
    """Custom error if a member doesn't have a defined role in the club."""

    def __init__(self, message):
        self.message = message
        super.__init__(message)


class Member(BaseModel):
    """Standard class of a Member stored in AWS Cognito.
    This class initializes the standard attributes that a Member should have.
    """

    # Cognito member uuid
    id: str

    # Standard member attributes provided by cognito
    details: CognitoMember

    # The following are the available roles of the club.
    manager: Optional[Manager]
    officer: Optional[Officer]
    academy_player: Optional[AcademyPlayer]
    player: Optional[Player]

    @classmethod
    @root_validator(pre=True)
    def check_member_has_a_role(cls, values):
        """Verify that the member has a role in the club."""

        # Define all possible roles for a member.
        roles = {"player", "manager", "officer", "academy_player"}

        # Check for role value in attributes passed in, if no role is found raise an exception.
        if any(value in values for value in roles):
            raise NoMemberRole(message="Member does not have a role.")
        return values
