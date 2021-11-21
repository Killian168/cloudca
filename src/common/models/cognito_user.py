from typing import Optional

from pydantic import BaseModel


class CognitoMember(BaseModel):
    """Standard class of a Member stored in AWS Cognito.
    This class initializes the standard attributes that a Member should have.
    """

    # Standard attributes given to every member by Cognito.
    # Related AWS Documentation:
    #       https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-attributes.html
    address: str
    birthdate: str
    email: str
    family_name: str
    gender: str
    given_name: str
    locale: str
    middle_name: Optional[str]
    name: Optional[str]
    nick_name: Optional[str]
    phone_number: Optional[str]
    picture: Optional[str]
    preferred_username: str
    profile: Optional[str]
    updated_at: Optional[int]
