import json

import cattrs

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
        member = cattrs.structure(member_details, Member)
    except Exception as e:
        # ToDo: Use cattrs.errors.ClassValidationError for catrs > 22.1.0
        for exc in e.exceptions:
            if isinstance(exc, NoMemberRole):
                LOGGER.error(f"Invalid member value passed in: {member_details} with error: {e}")
                return Lambda.format_response(
                    status_code=APIResponseCodes.BAD_REQUEST, error_message=str(exc)
                )
            else:
                LOGGER.error(e)
                return Lambda.format_response(
                    status_code=APIResponseCodes.BAD_REQUEST, error_message="Invalid input"
                )

    dynamodb = DynamoDB(logger=LOGGER)
    member_dict = cattrs.unstructure(member)
    dynamodb.put_item(table_name=MEMBERS_TABLE_NAME, item=member_dict)

    return Lambda.format_response(status_code=APIResponseCodes.OK, response_message=member_dict)
