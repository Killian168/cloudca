from enum import Enum, unique


@unique
class APIResponseCodes(Enum):
    """HTTP response codes for API responses as defined at:
    https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
    """

    OK = 200
    BAD_REQUEST = 400
