import json

from boto3.dynamodb.conditions import Key

from src.common.constants import MEMBERS_TABLE_NAME, TEAM_TABLE_NAME
from src.common.enums.api_response_codes import APIResponseCodes
from src.common.models.member import Member
from src.common.models.team import Team
from src.common.services.dynamodb import DynamoDB
from src.common.services.lambda_ import Lambda
from src.common.services.logger import get_logger

LOGGER = get_logger()


def get_members_by_team(event: dict, context):
    body = json.loads(event.get("body", None))
    team_id = body.get("TeamId", None)

    if team_id is None:
        return Lambda.format_response(
            status_code=APIResponseCodes.BAD_REQUEST, error_message=f"TeamId can not be: {team_id}"
        )

    dynamo = DynamoDB(logger=LOGGER)

    response = dynamo.scan_table(
        table_name=TEAM_TABLE_NAME,
        filter_expression=Key("id").eq(team_id),
    )

    if response:
        team = Team(**response[0])
    else:
        return Lambda.format_response(
            status_code=APIResponseCodes.BAD_REQUEST,
            error_message=f"No members found for TeamId: {team_id}",
        )

    conditions = [Key("id").eq(manager_id) for manager_id in team.managers]
    conditions.extend(Key("id").eq(player_id) for player_id in team.players)

    response = dynamo.scan_table(
        table_name=MEMBERS_TABLE_NAME,
        filter_expression=dynamo.create_or_filter_expression(conditions),
    )

    members_list = [Member(**obj).dict() for obj in response]
    return Lambda.format_response(status_code=APIResponseCodes.OK, response_message=members_list)
