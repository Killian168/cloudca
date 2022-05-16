import attrs


@attrs.define(slots=True)
class Fixture:
    """Represents what a fixture is"""

    home_team: str = attrs.field(default=None)
    away_team: str = attrs.field(default=None)
    competition: str = attrs.field(default=None)
    location: str = attrs.field(default=None)
    kick_off_time: str = attrs.field(default=None)
    meeting_time: str = attrs.field(default=None)
