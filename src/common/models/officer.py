from typing import List

from pydantic import BaseModel


class Officer(BaseModel):
    """Represents what a officer is in the club.
    Holds custom attributes that are related to a Officer role in the Club.
    """

    role: str
    responsibilities: List[str]
