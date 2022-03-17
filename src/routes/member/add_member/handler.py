import json

from pydantic import ValidationError

from src.common.constants import MEMBERS_TABLE_NAME
from src.common.enums.api_response_codes import APIResponseCodes
from src.common.models.member import Member, NoMemberRole
from src.common.services.dynamodb import DynamoDB
from src.common.services.lambda_ import Lambda
from src.common.services.logger import get_logger

LOGGER = get_logger()


def add_member(event, context):
    body = json.loads(event["body"])
    member_details = body.get("Member", None)

    if member_details is None:
        error_message = "Event processed does not have key `Member` or value passed in was: `None`"
        LOGGER.error(error_message)
        return Lambda.format_response(
            status_code=APIResponseCodes.BAD_REQUEST,
            error_message=error_message,
        )

    try:
        member = Member(**member_details)
    except NoMemberRole as e:
        LOGGER.error(f"Invalid member value passed in: {member_details} with error: {e}")
        return Lambda.format_response(
            status_code=APIResponseCodes.BAD_REQUEST, error_message=str(e)
        )
    except ValidationError as e:
        error_message = Lambda.parse_validation_error(e)
        LOGGER.error(error_message)
        return Lambda.format_response(
            status_code=APIResponseCodes.BAD_REQUEST, error_message=error_message
        )

    dynamodb = DynamoDB(logger=LOGGER)
    dynamodb.put_item(table_name=MEMBERS_TABLE_NAME, item=member.dict())

    return Lambda.format_response(status_code=APIResponseCodes.OK, response_message=member.dict())
