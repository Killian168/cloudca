from src.common.constants import MEMBERS_TABLE_NAME
from src.common.enums.api_response_codes import APIResponseCodes
from src.common.services.dynamodb import DeletionError, DynamoDB
from src.common.services.lambda_ import Lambda
from src.common.services.logger import get_logger

LOGGER = get_logger()


def delete_member(event, context):
    member_id = event.get("MemberId", None)
    if member_id is None:
        error_message = f"MemberId can not be: {member_id}"
        LOGGER.error(error_message)
        return Lambda.format_response(
            status_code=APIResponseCodes.BAD_REQUEST, error_message=error_message
        )

    dynamodb = DynamoDB(logger=LOGGER)

    try:
        dynamodb.delete_item(table_name=MEMBERS_TABLE_NAME, id=member_id)
    except DeletionError as e:
        return Lambda.format_response(
            status_code=APIResponseCodes.BAD_REQUEST, error_message=str(e)
        )

    return Lambda.format_response(
        status_code=APIResponseCodes.OK,
        response_message=f"Successfully deleted Member with id: {member_id}",
    )
