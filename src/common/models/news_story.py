from typing import List

from pydantic import BaseModel


class NewsStory(BaseModel):
    """Represents what a News Story is"""

    id: str
    category: List[str]
    title: str
    description: str
    thumbnail_key: str
