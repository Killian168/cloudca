from test.base_test_case import BaseTestCase
from test.test_fixtures.api_gateway_fixtures import APIGatewayFixtures
from test.test_fixtures.dynamo_fixtures import DynamoDbFixtures
from test.test_fixtures.fixtures import Fixtures

from parameterized import parameterized

from src.common.constants import TEAM_TABLE_NAME
from src.common.enums.api_response_codes import APIResponseCodes
from src.common.services.lambda_ import Lambda
from src.routes.team.get_team.handler import get_team


class TestGetTeamHandler(BaseTestCase):
    @classmethod
    def setUpClass(cls, *args, **kwargs):
        super().setUpClass(dynamo_tables=[TEAM_TABLE_NAME])

    def test_should_return_200_and_teams_list(self):
        # Set up
        team_id = "test_team_id"
        mock_event = {"TeamId": team_id}

        self.dynamodb_client.put_item(
            TableName=TEAM_TABLE_NAME,
            Item=DynamoDbFixtures.get_team_dynamodb_json(team_id),
        )

        # Call method
        request = APIGatewayFixtures.get_api_event(mock_event)
        response = get_team(request, None)

        # Assert Behaviour
        expected_response = Lambda.format_response(
            status_code=APIResponseCodes.OK, response_message=[Fixtures.get_team_json(team_id)]
        )
        self.assertDictEqual(response, expected_response)

    @parameterized.expand(
        [
            ("Invalid TeamId Key", {"notTeamId": "Test"}, "TeamId can not be: None"),
            ("Empty Event", {}, "TeamId can not be: None"),
            ("TeamId is None", {"TeamId": None}, "TeamId can not be: None"),
            ("Invalid TeamId", {"TeamId": "Not a Team"}, "Invalid TeamId: Not a Team"),
        ]
    )
    def test_should_return_400_and_error_message_on_bad_request(self, name, event, error_message):
        # Call method
        request = APIGatewayFixtures.get_api_event(event)
        response = get_team(request, None)

        # Assert behaviour
        expected_response = Lambda.format_response(
            status_code=APIResponseCodes.BAD_REQUEST,
            error_message=error_message,
        )
        self.assertEqual(expected_response, response)
