try:
    # Used for local testing
    from ..common.constants import MEMBERS_TABLE_NAME, TEAM_TABLE_NAME
    from ..common.enums.api_response_codes import APIResponseCodes
    from ..common.models.member import Member
    from ..common.models.team import Team
    from ..common.services.dynamodb import DynamoDB
    from ..common.services.lambda_ import Lambda
    from ..common.services.logger import get_logger
except ImportError:
    # Used for running in Lambda
    from common.models.member import Member
    from common.services.logger import get_logger
    from common.services.lambda_ import Lambda
    from common.enums.api_response_codes import APIResponseCodes
    from common.models.team import Team
    from common.constants import TEAM_TABLE_NAME, MEMBERS_TABLE_NAME

from boto3.dynamodb.conditions import Key

LOGGER = get_logger()


# Entry point for getMembersByTeam lambda
def get_members_by_team(event, context):
    # Sanitize input
    try:
        team_id = event["TeamId"]
        LOGGER.debug(f"TeamId value passed in event is: {team_id}")
    except KeyError:
        # Log error and return error response
        error_message = "Event processed does not have key `TeamId`."
        LOGGER.error(error_message)
        return Lambda.format_response(
            status_code=APIResponseCodes.BAD_REQUEST, error_message=error_message
        )

    dynamo = DynamoDB(logger=LOGGER)

    response = dynamo.scan_table(
        table_name=TEAM_TABLE_NAME,
        filter_expression=Key("id").eq(team_id),
    )
    team = Team(**response[0])

    conditions = [Key("id").eq(manager_id) for manager_id in team.managers]
    conditions.extend(Key("id").eq(player_id) for player_id in team.players)

    response = dynamo.scan_table(
        table_name=MEMBERS_TABLE_NAME,
        filter_expression=dynamo.create_or_filter_expression(conditions),
    )

    members_list = [Member(**obj).dict() for obj in response]
    return Lambda.format_response(status_code=APIResponseCodes.OK, response_message=members_list)
