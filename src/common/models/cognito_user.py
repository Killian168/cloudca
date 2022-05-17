from typing import Optional

import attrs


@attrs.define(slots=True)
class CognitoMember:
    """Standard class of a Member stored in AWS Cognito.
    This class initializes the standard attributes that a Member should have.
    """

    # Standard attributes given to every member by Cognito.
    # Related AWS Documentation:
    #       https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-attributes.html
    address: str = attrs.field()
    birthdate: str = attrs.field()
    email: str = attrs.field()
    family_name: str = attrs.field()
    gender: str = attrs.field()
    given_name: str = attrs.field()
    locale: str = attrs.field()
    preferred_username: str = attrs.field()
    middle_name: Optional[str] = attrs.field(default=None)
    name: Optional[str] = attrs.field(default=None)
    nick_name: Optional[str] = attrs.field(default=None)
    phone_number: Optional[str] = attrs.field(default=None)
    picture: Optional[str] = attrs.field(default=None)
    profile: Optional[str] = attrs.field(default=None)
    updated_at: Optional[int] = attrs.field(default=None)
