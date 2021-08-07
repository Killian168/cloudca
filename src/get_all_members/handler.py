try:
    # Used for local testing
    from ..common.models.member import Member
    from ..common.services.lambda_ import Lambda, LambdaResponseCodes
    from ..common.services.logger import get_logger
except ImportError:
    # Used for running in Lambda
    from common.models.member import Member
    from common.services.logger import get_logger
    from common.services.lambda_ import Lambda, LambdaResponseCodes

import boto3

MEMBERS_TABLE = "Members"
LOGGER = get_logger()


# Entry point for getMembersByTeam lambda
def get_all_members(event, context):
    # Scan DynamoDb members table for members where teamId==team_id
    # (var `team_id` instantiated above)
    dynamodb_resource = boto3.resource("dynamodb")
    table = dynamodb_resource.Table(MEMBERS_TABLE)
    response = table.scan()
    LOGGER.debug(f"Table scan responded with: {response}")

    # Create Member objects for each one of the members returned
    members_list = []
    for obj in response["Items"]:
        # Unpack obj key, value pairs into Member parameters for example
        # if obj = {"key": "val", "key1": "val1" }
        # the Member(**obj) would produce: Member(key=value, key1=val1)
        # Once the Member object is instantiated, append to members_list
        members_list.append(Member(**obj).dict())

    # Construct response and send back
    return Lambda.format_response(status_code=LambdaResponseCodes.OK, response_message=members_list)
