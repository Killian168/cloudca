from test.base_test_case import BaseTestCase
from test.test_fixtures.api_gateway_fixtures import APIGatewayFixtures
from test.test_fixtures.fixtures import Fixtures
from unittest.mock import patch

from parameterized import parameterized

from src.common.constants import MEMBERS_TABLE_NAME
from src.common.enums.api_response_codes import APIResponseCodes
from src.common.services.lambda_ import Lambda
from src.routes.member.add_member.handler import add_member


class TestAddMembersHandler(BaseTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def setUpClass(cls, *args, **kwargs):
        super().setUpClass(dynamo_tables=[MEMBERS_TABLE_NAME])

    def test_should_return_200_and_members_list(self):
        # Set up
        test_uuid = "16ba49bc-5464-4ee2-9846-77264b3ac62d"

        # Call method
        with patch("src.common.models.member.uuid4") as mock_uuid4:
            mock_uuid4.return_value = test_uuid
            request_body = {"Member": Fixtures.get_member_no_id()}
            request = APIGatewayFixtures.get_api_event(request_body)
            response = add_member(request, None)

        # Assert Behaviour
        expected_response = Lambda.format_response(
            status_code=APIResponseCodes.OK,
            response_message=Fixtures.get_player_json(test_uuid),
        )
        self.assertEqual(response, expected_response)

        response = self.dynamodb_client.scan(
            TableName=MEMBERS_TABLE_NAME,
            ExpressionAttributeValues={
                ":id": {
                    "S": test_uuid,
                },
            },
            FilterExpression="id = :id",
        )
        self.assertEqual(len(response["Items"]), 1)

    @parameterized.expand(
        [
            (
                "Empty Event",
                APIGatewayFixtures.get_api_event({}),
                "Event processed does not have key `Member`.",
            ),
            (
                "Member is None",
                APIGatewayFixtures.get_api_event({"Member": None}),
                "Member can not be: None",
            ),
            (
                "Missing Details",
                APIGatewayFixtures.get_api_event({"Member": {}}),
                "Member does not have a role.",
            ),
            (
                "Invalid Member",
                APIGatewayFixtures.get_api_event({"Member": {"details": {}}}),
                "Member does not have a role.",
            ),
            (
                "No Role Member",
                APIGatewayFixtures.get_api_event({"Member": Fixtures.get_member_no_role_json()}),
                "Member does not have a role.",
            ),
        ]
    )
    def test_should_return_400_and_error_message_on_bad_request(self, name, event, error_message):
        # Call method
        response = add_member(event, None)

        # Assert Behaviour
        expected_response = Lambda.format_response(
            status_code=APIResponseCodes.BAD_REQUEST,
            error_message=error_message,
        )
        self.assertEqual(response, expected_response)

        response = self.dynamodb_client.scan(TableName=MEMBERS_TABLE_NAME)
        self.assertEqual(len(response["Items"]), 0)
