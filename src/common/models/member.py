from typing import Optional
from uuid import uuid4

import attrs

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


@attrs.define(slots=True)
class Member:
    """Standard class of a Member.
    This class initializes the standard attributes that a Member should have.
    """

    # Standard member attributes provided by cognito
    details: CognitoMember

    # Cognito member uuid
    id: Optional[str] = attrs.field(default=None)

    # The following are the available roles of the club.
    manager: Optional[Manager] = attrs.field(default=None)
    officer: Optional[Officer] = attrs.field(default=None)
    academy_player: Optional[AcademyPlayer] = attrs.field(default=None)
    player: Optional[Player] = attrs.field(default=None)

    def __attrs_post_init__(self):
        # Check for role value in attributes passed in, if no role is found raise an exception.
        is_manager = bool(self.manager)
        is_officer = bool(self.officer)
        is_academy_player = bool(self.academy_player)
        is_player = bool(self.player)

        if not (is_manager or is_officer or is_academy_player or is_player):
            raise NoMemberRole()

    @id.validator
    def _validate_id(self, attribute, value):
        if not value:
            self.id = str(uuid4())
