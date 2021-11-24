from test.test_fixtures.dynamo_fixtures import DynamoDbFixtures
from test.test_fixtures.fixtures import Fixtures
from unittest import TestCase

import boto3
from moto import mock_dynamodb2

from src.common.constants import MEMBERS_TABLE_NAME, TEAM_TABLE_NAME
from src.common.services.lambda_ import Lambda
from src.get_members_by_team.handler import get_members_by_team


class TestHandlerBaseCase(TestCase):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()


class TestGetMembersByTeamHandler(TestHandlerBaseCase):
    def test_should_return_400_and_error_message_on_bad_request(self):
        # Set up
        mock_event = {"notTeamId": "Test"}

        # Call method
        response = get_members_by_team(mock_event, None)

        # Assert behaviour
        self.assertEqual(response[Lambda.KEY_STATUS_CODE], 400)
        self.assertEqual(
            response[Lambda.KEY_BODY],
            {"errorMessage": "Event processed does not have key `TeamId`."},
        )

    @mock_dynamodb2
    def test_should_return_200_and_members_list(self):
        # Set up
        team_id = "test-team"
        manager_id = "manager-id-1"
        player_id = "player-id-1"
        mock_event = {"TeamId": team_id}
        dynamodb_client = boto3.client("dynamodb")

        # Set up dynamoDb Tables
        dynamodb_client.create_table(
            TableName=MEMBERS_TABLE_NAME,
            KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
        )

        dynamodb_client.create_table(
            TableName=TEAM_TABLE_NAME,
            KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
        )

        dynamodb_client.put_item(
            TableName=MEMBERS_TABLE_NAME,
            Item=DynamoDbFixtures.get_manager_dynamo_json(manager_id),
        )

        dynamodb_client.put_item(
            TableName=MEMBERS_TABLE_NAME,
            Item=DynamoDbFixtures.get_player_dynamo_json(player_id),
        )

        dynamodb_client.put_item(
            TableName=TEAM_TABLE_NAME,
            Item=DynamoDbFixtures.get_team_dynamodb_json(
                team_id=team_id, managers=[manager_id], players=[player_id]
            ),
        )

        # Call method
        response = get_members_by_team(mock_event, None)

        # Assert Behaviour
        expected_response = {
            "body": {
                "message": [
                    Fixtures.get_manager_json(manager_id),
                    Fixtures.get_player_json(player_id),
                ]
            },
            "statusCode": 200,
        }
        self.assertEqual(response, expected_response)
