from typing import List, Optional
from uuid import uuid4

import attrs

from ..models.fixture import Fixture


@attrs.define(slots=True)
class Team:
    """Represents what a team is in the club.
    Holds custom attributes that are related to a Team in the Club.
    """

    name: str = attrs.field()
    managers: List[str] = attrs.field(default=[])
    players: List[str] = attrs.field(default=[])
    training_times: List[str] = attrs.field(default=[])
    fixtures: List[Fixture] = attrs.field(default=[])
    id: Optional[str] = attrs.field(default=None)

    @id.validator
    def _validate_id(self, attribute, value):
        if not value:
            self.id = str(uuid4())
