from enum import Enum, unique


@unique
class NewsCategories(Enum):
    """Valid categories to list a news item under
    """
    all = "all"
    academy = "academy"
    general = "general"

    @classmethod
    def has_value(cls, value):
        return value in cls.__members__
