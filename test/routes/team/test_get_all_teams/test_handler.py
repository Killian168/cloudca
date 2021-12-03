from test.base_test_case import BaseTestCase
from test.test_fixtures.dynamo_fixtures import DynamoDbFixtures
from test.test_fixtures.fixtures import Fixtures

from src.common.constants import TEAM_TABLE_NAME
from src.common.enums.api_response_codes import APIResponseCodes
from src.common.services.lambda_ import Lambda
from src.routes.team.get_all_teams.handler import get_all_teams


class TestGetAllTeamsHandler(BaseTestCase):
    @classmethod
    def setUpClass(cls, *args, **kwargs):
        super().setUpClass(dynamo_tables=[TEAM_TABLE_NAME])

    def test_should_return_200_and_teams_list(self):
        # Set up
        team_id = "test_team_id"
        self.dynamodb_client.put_item(
            TableName=TEAM_TABLE_NAME,
            Item=DynamoDbFixtures.get_team_dynamodb_json(team_id),
        )

        # Call method
        response = get_all_teams(None, None)

        # Assert Behaviour
        expected_response = Lambda.format_response(
            status_code=APIResponseCodes.OK, response_message=[Fixtures.get_team_json(team_id)]
        )
        self.maxDiff = None
        self.assertEqual(response, expected_response)
