import json

import cattrs

from src.common.constants import TEAM_TABLE_NAME
from src.common.enums.api_response_codes import APIResponseCodes
from src.common.models.team import Team
from src.common.services.dynamodb import DynamoDB
from src.common.services.lambda_ import Lambda
from src.common.services.logger import get_logger

LOGGER = get_logger()


def add_team(event, context):
    body = json.loads(event.get("body", None))
    team_details = body.get("Team", None)

    if team_details is None:
        error_message = "Event processed does not have key `Team` or object is empty"
        LOGGER.error(error_message)
        return Lambda.format_response(
            status_code=APIResponseCodes.BAD_REQUEST, error_message=error_message
        )

    try:
        team = cattrs.structure(team_details, Team)
    except Exception as e:
        # ToDo: Use cattrs.errors.ClassValidationError for catrs > 22.1.0
        LOGGER.error(e)
        return Lambda.format_response(
            status_code=APIResponseCodes.BAD_REQUEST, error_message="Invalid input"
        )

    dynamodb = DynamoDB(logger=LOGGER)
    dynamodb.put_item(table_name=TEAM_TABLE_NAME, item=cattrs.unstructure(team))

    return Lambda.format_response(
        status_code=APIResponseCodes.OK, response_message=cattrs.unstructure(team)
    )
