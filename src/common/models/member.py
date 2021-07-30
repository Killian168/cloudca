from pydantic import BaseModel


class Member(BaseModel):
    id: str
    firstName: str
    lastName: str
    teamId: str
