from test.test_fixtures.dynamo_fixtures import DynamoDbFixtures
from test.test_fixtures.fixtures import Fixtures
from unittest import TestCase

import boto3
from moto import mock_dynamodb2

from src.get_all_members.handler import get_all_members
from src.get_members_by_team.handler import MEMBERS_TABLE


class TestHandlerBaseCase(TestCase):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()


class TestGetAllMembersHandler(TestHandlerBaseCase):
    @mock_dynamodb2
    def test_should_return_200_and_members_list(self):
        # Set up
        member_id = "test_member_id"
        dynamodb_client = boto3.client("dynamodb")
        dynamodb_client.create_table(
            TableName=MEMBERS_TABLE,
            KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
        )
        dynamodb_client.put_item(
            TableName=MEMBERS_TABLE,
            Item=DynamoDbFixtures.get_member_no_role_dynamo_json(member_id),
        )

        # Call method
        response = get_all_members(None, None)
        print(f"response = {response}")

        # Assert Behaviour
        expected_response = {
            "statusCode": 200,
            "body": {"message": [Fixtures.get_member_no_role_json(member_id)]},
        }
        self.assertEqual(response, expected_response)
