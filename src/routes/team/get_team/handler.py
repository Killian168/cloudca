import json

from boto3.dynamodb.conditions import Key

from src.common.constants import TEAM_TABLE_NAME
from src.common.enums.api_response_codes import APIResponseCodes
from src.common.services.dynamodb import DynamoDB
from src.common.services.lambda_ import Lambda
from src.common.services.logger import get_logger

LOGGER = get_logger()


def get_team(event, context):
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

    # Check response is not empty
    if not response:
        return Lambda.format_response(
            status_code=APIResponseCodes.BAD_REQUEST, error_message=f"Invalid TeamId: {team_id}"
        )

    return Lambda.format_response(status_code=APIResponseCodes.OK, response_message=response)
