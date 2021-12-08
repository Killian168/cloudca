from boto3.dynamodb.conditions import Key

from src.common.constants import MEMBERS_TABLE_NAME, TEAM_TABLE_NAME
from src.common.enums.api_response_codes import APIResponseCodes
from src.common.models.member import Member
from src.common.models.team import Team
from src.common.services.dynamodb import DynamoDB, ScanningError
from src.common.services.lambda_ import Lambda
from src.common.services.logger import get_logger

LOGGER = get_logger()


def get_members_by_team(event: dict, context):
    team_id = event.get("TeamId", None)

    if team_id is None:
        return Lambda.format_response(
            status_code=APIResponseCodes.BAD_REQUEST, error_message=f"TeamId can not be: {team_id}"
        )

    dynamo = DynamoDB(logger=LOGGER)

    try:
        response = dynamo.scan_table(
            table_name=TEAM_TABLE_NAME,
            filter_expression=Key("id").eq(team_id),
        )
    except ScanningError:
        return Lambda.format_response(
            status_code=APIResponseCodes.BAD_REQUEST, error_message=f"Invalid TeamId: {team_id}"
        )

    team = Team(**response[0])

    conditions = [Key("id").eq(manager_id) for manager_id in team.managers]
    conditions.extend(Key("id").eq(player_id) for player_id in team.players)

    response = dynamo.scan_table(
        table_name=MEMBERS_TABLE_NAME,
        filter_expression=dynamo.create_or_filter_expression(conditions),
    )

    members_list = [Member(**obj).dict() for obj in response]
    return Lambda.format_response(status_code=APIResponseCodes.OK, response_message=members_list)
