from test.test_fixtures.api_gateway_fixtures import APIGatewayFixtures
from test.test_fixtures.fixtures import Fixtures
from test.unit_test.base_test_case import BaseTestCase
from unittest.mock import patch

from parameterized import parameterized

from src.common.constants import TEAM_TABLE_NAME
from src.common.enums.api_response_codes import APIResponseCodes
from src.common.services.lambda_ import Lambda
from src.routes.team.add_team.handler import add_team


class TestAddTeamHandler(BaseTestCase):
    @classmethod
    def setUpClass(cls, *args, **kwargs):
        super().setUpClass(dynamo_tables=[TEAM_TABLE_NAME])

    def test_should_return_200_and_team(self):
        # Set up
        test_uuid = "16ba49bc-5464-4ee2-9846-77264b3ac62d"

        # Call method
        with patch("src.common.models.team.uuid4") as mock_uuid4:
            mock_uuid4.return_value = test_uuid
            request = APIGatewayFixtures.get_api_event({"Team": Fixtures.get_team_no_id_json()})
            response = add_team(request, None)

        # Assert Behaviour
        expected_response = Lambda.format_response(
            status_code=APIResponseCodes.OK,
            response_message=Fixtures.get_team_json(test_uuid),
        )
        self.assertEqual(response, expected_response)

        response = self.dynamodb_client.scan(
            TableName=TEAM_TABLE_NAME,
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
                {},
                "Event processed does not have key `Team` or object is empty",
            ),
            (
                "Team is None",
                {"Team": None},
                "Event processed does not have key `Team` or object is empty",
            ),
            (
                "Invalid Team",
                {"Team": {}},
                {"field required": ["name"]},
            ),
        ]
    )
    def test_should_return_400_and_error_message_on_bad_request(self, name, event, error_message):
        # Call method
        request = APIGatewayFixtures.get_api_event(event)
        response = add_team(request, None)

        # Assert Behaviour
        expected_response = Lambda.format_response(
            status_code=APIResponseCodes.BAD_REQUEST,
            error_message=error_message,
        )
        self.assertEqual(response, expected_response)

        response = self.dynamodb_client.scan(TableName=TEAM_TABLE_NAME)
        self.assertEqual(len(response["Items"]), 0)
