import cattrs

from src.common.constants import MEMBERS_TABLE_NAME
from src.common.enums.api_response_codes import APIResponseCodes
from src.common.models.member import Member
from src.common.services.dynamodb import DynamoDB
from src.common.services.lambda_ import Lambda
from src.common.services.logger import get_logger

LOGGER = get_logger()


def get_all_members(event, context):
    dynamodb = DynamoDB(logger=LOGGER)
    items = dynamodb.scan_table(table_name=MEMBERS_TABLE_NAME)

    members_list = []
    for obj in items:
        member = cattrs.structure(obj, Member)
        members_list.append(cattrs.unstructure(member))

    return Lambda.format_response(status_code=APIResponseCodes.OK, response_message=members_list)
