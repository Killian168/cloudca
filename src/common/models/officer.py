from typing import List

import attrs


@attrs.define
class Officer:
    """Represents what a officer is in the club.
    Holds custom attributes that are related to a Officer role in the Club.
    """

    role: str
    responsibilities: List[str]
