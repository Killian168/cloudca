import boto3

from src.common.constants import MEMBERS_TABLE_NAME
from src.common.enums.api_response_codes import APIResponseCodes
from src.common.models.member import Member
from src.common.services.lambda_ import Lambda
from src.common.services.logger import get_logger

LOGGER = get_logger()


def get_all_members(event, context):
    dynamodb_resource = boto3.resource("dynamodb")
    table = dynamodb_resource.Table(MEMBERS_TABLE_NAME)
    response = table.scan()
    LOGGER.debug(f"Table scan responded with: {response}")

    members_list = []
    for obj in response["Items"]:
        members_list.append(Member(**obj).dict())

    return Lambda.format_response(status_code=APIResponseCodes.OK, response_message=members_list)
