from test.base_test_case import BaseTestCase
from test.test_fixtures.dynamo_fixtures import DynamoDbFixtures
from test.test_fixtures.fixtures import Fixtures

from parameterized import parameterized

from src.common.constants import MEMBERS_TABLE_NAME, TEAM_TABLE_NAME
from src.common.enums.api_response_codes import APIResponseCodes
from src.common.services.lambda_ import Lambda
from src.routes.member.get_members_by_team.handler import get_members_by_team


class TestGetMembersByTeamHandler(BaseTestCase):
    @classmethod
    def setUpClass(cls, *args, **kwargs):
        super().setUpClass(dynamo_tables=[MEMBERS_TABLE_NAME, TEAM_TABLE_NAME])

    def test_should_return_200_and_members_list(self):
        # Set up
        team_id = "test-team"
        manager_id = "manager-id-1"
        player_id = "player-id-1"
        mock_event = {"TeamId": team_id}

        self.dynamodb_client.put_item(
            TableName=MEMBERS_TABLE_NAME,
            Item=DynamoDbFixtures.get_manager_dynamo_json(manager_id),
        )

        self.dynamodb_client.put_item(
            TableName=MEMBERS_TABLE_NAME,
            Item=DynamoDbFixtures.get_player_dynamo_json(player_id),
        )

        self.dynamodb_client.put_item(
            TableName=TEAM_TABLE_NAME,
            Item=DynamoDbFixtures.get_team_dynamodb_json(
                team_id=team_id, managers=[manager_id], players=[player_id]
            ),
        )

        # Call method
        response = get_members_by_team(mock_event, None)

        # Assert Behaviour
        expected_response = Lambda.format_response(
            status_code=APIResponseCodes.OK,
            response_message=[
                Fixtures.get_manager_json(manager_id),
                Fixtures.get_player_json(player_id),
            ],
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
    def test_should_return_400_and_error_message_on_bad_request(
        self, name, mock_event, error_message
    ):
        # Call method
        response = get_members_by_team(mock_event, None)

        # Assert behaviour
        expected_response = Lambda.format_response(
            status_code=APIResponseCodes.BAD_REQUEST,
            error_message=error_message,
        )
        self.assertEqual(expected_response, response)
