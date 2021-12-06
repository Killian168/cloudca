from src.common.constants import TEAM_TABLE_NAME
from src.common.enums.api_response_codes import APIResponseCodes
from src.common.models.team import Team
from src.common.services.dynamodb import DynamoDB
from src.common.services.lambda_ import Lambda
from src.common.services.logger import get_logger

LOGGER = get_logger()


def get_all_teams(event, context):
    dynamodb = DynamoDB(logger=LOGGER)
    items = dynamodb.scan_table(table_name=TEAM_TABLE_NAME)

    members_list = []
    for obj in items:
        members_list.append(Team(**obj).dict())
    return Lambda.format_response(status_code=APIResponseCodes.OK, response_message=members_list)
