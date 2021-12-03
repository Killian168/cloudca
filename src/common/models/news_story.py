from typing import List, Optional
from uuid import uuid4

from pydantic import BaseModel, root_validator

from src.common.constants import NEWS_THUMBNAILS_KEY


class NewsStory(BaseModel):
    """Represents what a News Story is"""

    id: Optional[str]
    category: List[str]
    title: str
    description: str
    thumbnail_key: Optional[str]

    @root_validator
    def check_member_has_a_role(cls, values):
        """Verify that the news story has an id and a thumbnail key"""
        if values["id"] is None:
            values["id"] = str(uuid4())

        if values["thumbnail_key"] is None:
            values["thumbnail_key"] = f'{NEWS_THUMBNAILS_KEY}/{values["id"]}.txt'

        return values
