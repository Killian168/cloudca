from boto3.dynamodb.conditions import Key

from src.common.constants import TEAM_TABLE_NAME
from src.common.enums.api_response_codes import APIResponseCodes
from src.common.services.dynamodb import DynamoDB
from src.common.services.lambda_ import Lambda
from src.common.services.logger import get_logger

LOGGER = get_logger()


def get_team(event, context):
    try:
        team_id = event["TeamId"]
        LOGGER.debug(f"TeamId value passed in event is: {team_id}")
    except KeyError:
        error_message = "Event processed does not have key `TeamId`."
        LOGGER.error(error_message)
        return Lambda.format_response(
            status_code=APIResponseCodes.BAD_REQUEST, error_message=error_message
        )

    dynamo = DynamoDB()
    response = dynamo.scan_table(
        table_name=TEAM_TABLE_NAME, filter_expression=Key("id").eq(team_id)
    )
    return Lambda.format_response(status_code=APIResponseCodes.OK, response_message=response)
