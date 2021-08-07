from unittest import TestCase

from src.get_all_members.handler import get_all_members
from src.get_members_by_team.handler import MEMBERS_TABLE
from json import dumps
from moto import mock_dynamodb2
import boto3


class TestHandlerBaseCase(TestCase):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()


class TestGetAllMembersHandler(TestHandlerBaseCase):
    @mock_dynamodb2
    def test_should_return_200_and_members_list(self):
        # Set up
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
                "address": {"S": "test-id"},
                "birthdate": {"S": "test-first-name"},
                "email": {"S": "test-last-name"},
                "family_name": {"S": "test_team_id"},
                "gender": {"S": "test_team_id"},
                "given_name": {"S": "test_team_id"},
                "locale": {"S": "test_team_id"},
                "role": {"S": "test_team_id"},
                "responsibilities": {"S": "test_team_id"},
            },
        )

        # Call method
        response = get_all_members(None, None)
        print(f'response = {response}')

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
                            "teamId": "test_team_id",
                        }
                    ]
                )
            },
        }
        self.assertEqual(response, expected_response)
