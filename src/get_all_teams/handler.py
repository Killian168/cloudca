try:
    # Used for local testing
    from ..common.constants import TEAM_TABLE_NAME
    from ..common.enums.api_response_codes import APIResponseCodes
    from ..common.models.team import Team
    from ..common.services.lambda_ import Lambda
    from ..common.services.logger import get_logger
except ImportError:
    # Used for running in Lambda
    from common.models.member import Member
    from common.services.logger import get_logger
    from common.services.lambda_ import Lambda
    from common.enums.api_response_codes import APIResponseCodes
    from common.constants import TEAM_TABLE_NAME

import boto3

LOGGER = get_logger()


def get_all_teams(event, context):
    dynamodb_resource = boto3.resource("dynamodb")
    table = dynamodb_resource.Table(TEAM_TABLE_NAME)
    response = table.scan()
    LOGGER.debug(f"Table scan responded with: {response}")

    members_list = []
    for obj in response["Items"]:
        members_list.append(Team(**obj).dict())

    return Lambda.format_response(status_code=APIResponseCodes.OK, response_message=members_list)
