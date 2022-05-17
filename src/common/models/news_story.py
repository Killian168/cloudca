from typing import List, Optional
from uuid import uuid4

import attrs

from src.common.constants import NEWS_THUMBNAILS_KEY


@attrs.define(slots=True)
class NewsStory:
    """Represents what a News Story is"""

    category: List[str] = attrs.field()
    title: str = attrs.field()
    description: str = attrs.field()
    id: Optional[str] = attrs.field(default=None)
    thumbnail_key: Optional[str] = attrs.field(default=None)

    @thumbnail_key.validator
    def _create_thumbnail_key(self, attribute, value):
        if not value:
            self.thumbnail_key = f"{NEWS_THUMBNAILS_KEY}/{self.id}.txt"

    @id.validator
    def _validate_id(self, attribute, value):
        if not value:
            self.id = str(uuid4())
