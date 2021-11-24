from pydantic import BaseModel


class Fixture(BaseModel):
    """Represents what a fixture is"""

    home_team: str
    away_team: str
    competition: str
    location: str
    kick_off_time: str
    meeting_time: str = None
