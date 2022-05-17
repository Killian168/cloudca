from typing import List

import attrs


@attrs.define(slots=True)
class Manager:
    """Represents what a manager is in the club.
    Holds custom attributes that are related to a Manger role in the Club.
    """

    favorite_formation: str
    win_record: int
    loss_record: int
    achievements: List[str]
