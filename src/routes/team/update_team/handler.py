from pydantic import ValidationError

from src.common.constants import TEAM_TABLE_NAME
from src.common.enums.api_response_codes import APIResponseCodes
from src.common.models.team import Team
from src.common.services.dynamodb import DynamoDB, UpdateError
from src.common.services.lambda_ import Lambda
from src.common.services.logger import get_logger

LOGGER = get_logger()


def update_team(event, context):
    team_details = event.get("Team", None)

    if team_details is None:
        error_message = "Event processed does not have key `Team` or object is empty"
        LOGGER.error(error_message)
        return Lambda.format_response(
            status_code=APIResponseCodes.BAD_REQUEST, error_message=error_message
        )

    try:
        team = Team(**team_details)
    except ValidationError as e:
        error_message = {}
        for err in e.errors():
            if error_message.get(err["msg"], None) is None:
                error_message[err["msg"]] = []
            if len(err["loc"]) > 1:
                error_message[err["msg"]].append(dict([err["loc"]]))
            elif "id" not in err["loc"][0]:
                error_message[err["msg"]].append(err["loc"][0])

        LOGGER.error(error_message)
        return Lambda.format_response(
            status_code=APIResponseCodes.BAD_REQUEST, error_message=error_message
        )

    dynamodb = DynamoDB(logger=LOGGER)
    try:
        dynamodb.update_item(table_name=TEAM_TABLE_NAME, item=team.dict())
    except UpdateError as e:
        return Lambda.format_response(
            status_code=APIResponseCodes.BAD_REQUEST, error_message=str(e)
        )

    return Lambda.format_response(status_code=APIResponseCodes.OK, response_message=team.dict())
