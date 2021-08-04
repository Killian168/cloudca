from pydantic import BaseModel


class Member(BaseModel):
    """ Class that defines what a club member is. This class is also used as a schema for holding data
        in DynamoDB table Members. """
    id: str
    firstName: str
    lastName: str
    teamId: str
