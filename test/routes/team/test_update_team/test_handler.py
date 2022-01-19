from test.base_test_case import BaseTestCase
from test.test_fixtures.dynamo_fixtures import DynamoDbFixtures
from test.test_fixtures.fixtures import Fixtures

from parameterized import parameterized

from src.common.constants import TEAM_TABLE_NAME
from src.common.enums.api_response_codes import APIResponseCodes
from src.common.services.lambda_ import Lambda
from src.routes.team.update_team.handler import update_team


class TestUpdateTeamHandler(BaseTestCase):
    TEST_UUID = "16ba49bc-5464-4ee2-9846-77264b3ac62d"

    @classmethod
    def setUpClass(cls, *args, **kwargs):
        super().setUpClass(dynamo_tables=[TEAM_TABLE_NAME])

    def test_should_return_200_and_team(self):
        # Set Up
        team_name = "testing-name"
        self.dynamodb_client.put_item(
            TableName=TEAM_TABLE_NAME,
            Item=DynamoDbFixtures.get_team_dynamodb_json(TestUpdateTeamHandler.TEST_UUID),
        )

        # Call method
        response = update_team(
            {"Team": Fixtures.get_team_json(TestUpdateTeamHandler.TEST_UUID, team_name)}, None
        )

        # Assert Behaviour
        expected_response = Lambda.format_response(
            status_code=APIResponseCodes.OK,
            response_message=Fixtures.get_team_json(TestUpdateTeamHandler.TEST_UUID, team_name),
        )
        self.assertEqual(response, expected_response)

        response = self.dynamodb_client.scan(
            TableName=TEAM_TABLE_NAME,
            ExpressionAttributeValues={
                ":id": {
                    "S": TestUpdateTeamHandler.TEST_UUID,
                },
            },
            FilterExpression="id = :id",
        )
        self.assertEqual(len(response["Items"]), 1)
        self.assertEqual(response["Items"][0]["name"]["S"], team_name)

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
            (
                "Should not put entry in table",
                {"Team": Fixtures.get_team_json(TEST_UUID)},
                f"Error updating item with id:{TEST_UUID} in table Teams, responded with: No item"
                f" with id {TEST_UUID} found",
            ),
        ]
    )
    def test_should_return_400_and_error_message_on_bad_request(self, name, event, error_message):
        # Call method
        response = update_team(event, None)

        # Assert Behaviour
        expected_response = Lambda.format_response(
            status_code=APIResponseCodes.BAD_REQUEST,
            error_message=error_message,
        )
        self.assertEqual(response, expected_response)

        response = self.dynamodb_client.scan(TableName=TEAM_TABLE_NAME)
        self.assertEqual(len(response["Items"]), 0)
