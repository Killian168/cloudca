from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, root_validator, validator

from ..models.academy_player import AcademyPlayer
from ..models.cognito_user import CognitoMember
from ..models.manager import Manager
from ..models.officer import Officer
from ..models.player import Player

MEMBER_ROLES = {"player", "manager", "officer", "academy_player"}


class NoMemberRole(Exception):
    """Custom error if a member doesn't have a defined role in the club."""

    def __init__(self):
        super().__init__("Member does not have a role.")


class Member(BaseModel):
    """Standard class of a Member.
    This class initializes the standard attributes that a Member should have.
    """

    # Cognito member uuid
    id: Optional[str]

    # Standard member attributes provided by cognito
    details: CognitoMember

    # The following are the available roles of the club.
    manager: Optional[Manager]
    officer: Optional[Officer]
    academy_player: Optional[AcademyPlayer]
    player: Optional[Player]

    @root_validator
    def check_member_has_a_role(cls, values):
        """Verify that the member has a role in the club.
        Check for role value in attributes passed in, if no role is found raise an exception."""

        # Check for role value in attributes passed in, if no role is found raise an exception.
        for role in MEMBER_ROLES:
            role_value = values.get(role, None)
            if role_value is not None:
                return values
        raise NoMemberRole()

    @validator("id", always=True)
    def check_member_has_id(cls, value):
        return value or str(uuid4())
