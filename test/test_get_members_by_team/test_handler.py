from json import dumps
from unittest import TestCase

import boto3
from moto import mock_dynamodb2

from src.common.services.lambda_ import Lambda
from src.get_members_by_team.handler import MEMBERS_TABLE, get_members_by_team


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
            {"errorMessage": dumps("Event processed does not have key `TeamId`.")},
        )

    @mock_dynamodb2
    def test_should_return_200_and_members_list(self):
        # Set up
        test_team_id = "test-team"
        mock_event = {"TeamId": test_team_id}
        dynamodb_client = boto3.client("dynamodb")

        # Set up dynamoDb Table
        dynamodb_client.create_table(
            TableName=MEMBERS_TABLE,
            KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
        )

        # Put item in table
        dynamodb_client.put_item(
            TableName=MEMBERS_TABLE,
            Item={
                "id": {"S": "test-id"},
                "firstName": {"S": "test-first-name"},
                "lastName": {"S": "test-last-name"},
                "teamId": {"S": test_team_id},
            },
        )

        # Call method
        response = get_members_by_team(mock_event, None)

        # Assert Behaviour
        expected_response = {
            "statusCode": 200,
            "body": {
                "message": dumps(
                    [
                        {
                            "id": "test-id",
                            "firstName": "test-first-name",
                            "lastName": "test-last-name",
                            "teamId": "test-team",
                        }
                    ]
                )
            },
        }
        self.assertEqual(response, expected_response)
