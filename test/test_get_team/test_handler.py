from test.test_fixtures.dynamo_fixtures import DynamoDbFixtures
from test.test_fixtures.fixtures import Fixtures
from unittest import TestCase

import boto3
from moto import mock_dynamodb2

from src.common.constants import TEAM_TABLE_NAME
from src.common.services.lambda_ import Lambda
from src.get_team.handler import get_team


class TestHandlerBaseCase(TestCase):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()


class TestGetAllTeamsHandler(TestHandlerBaseCase):
    def test_should_return_400_and_error_message_on_bad_request(self):
        # Set up
        mock_event = {"notTeamId": "Test"}

        # Call method
        response = get_team(mock_event, None)

        # Assert behaviour
        self.assertEqual(response[Lambda.KEY_STATUS_CODE], 400)
        self.assertEqual(
            response[Lambda.KEY_BODY],
            {"errorMessage": "Event processed does not have key `TeamId`."},
        )

    @mock_dynamodb2
    def test_should_return_200_and_teams_list(self):
        # Set up
        team_id = "test_team_id"
        mock_event = {"TeamId": team_id}
        dynamodb_client = boto3.client("dynamodb")
        dynamodb_client.create_table(
            TableName=TEAM_TABLE_NAME,
            KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
        )
        dynamodb_client.put_item(
            TableName=TEAM_TABLE_NAME,
            Item=DynamoDbFixtures.get_team_dynamodb_json(team_id),
        )

        # Call method
        response = get_team(mock_event, None)
        print(f"response = {response}")

        # Assert Behaviour
        expected_response = {
            "statusCode": 200,
            "body": {"message": [Fixtures.get_team_json(team_id)]},
        }
        self.assertEqual(response, expected_response)