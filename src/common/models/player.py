from typing import List

from pydantic import BaseModel


class Player(BaseModel):
    """Represents what a player is in the club.
    Holds custom attributes that are related to a Player role in the Club.
    """

    positions: List[str] = []
    training_times: List[str] = []
    match_times: List[str] = []
    teams: List[str] = []
    season_appearances: int = 0
    season_assists: int = 0
    season_goals: int = 0
    all_time_appearances: int = 0
    all_time_assists: int = 0
    all_time_goals: int = 0
    achievements: List[str] = []
