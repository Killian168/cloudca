from pydantic import ValidationError

from src.common.constants import MEMBERS_TABLE_NAME
from src.common.enums.api_response_codes import APIResponseCodes
from src.common.models.member import Member
from src.common.services.dynamodb import DynamoDB, UpdateError
from src.common.services.lambda_ import Lambda
from src.common.services.logger import get_logger

LOGGER = get_logger()


def update_member(event, context):

    try:
        member_details = event["Member"]
        LOGGER.debug(f"Member value passed in event is: {member_details}")
    except KeyError:
        error_message = "Event processed does not have key `Member`."
        LOGGER.error(error_message)
        return Lambda.format_response(
            status_code=APIResponseCodes.BAD_REQUEST, error_message=error_message
        )

    if member_details is None:
        return Lambda.format_response(
            status_code=APIResponseCodes.BAD_REQUEST,
            error_message=f"Member can not be: {member_details}",
        )

    try:
        member = Member(**member_details)
    except ValidationError as e:

        error_message = {}
        for err in e.errors():
            if error_message.get(err["msg"], None) is None:
                error_message[err["msg"]] = []
            if len(err["loc"]) > 1:
                error_message[err["msg"]].append(dict([err["loc"]]))
            else:
                error_message[err["msg"]].append(err["loc"][0])

        LOGGER.error(error_message)
        return Lambda.format_response(
            status_code=APIResponseCodes.BAD_REQUEST, error_message=error_message
        )

    dynamodb = DynamoDB(logger=LOGGER)

    try:
        dynamodb.update_item(table_name=MEMBERS_TABLE_NAME, item=member.dict())
    except UpdateError as e:
        return Lambda.format_response(
            status_code=APIResponseCodes.BAD_REQUEST, error_message=str(e)
        )

    return Lambda.format_response(status_code=APIResponseCodes.OK, response_message=member.dict())
