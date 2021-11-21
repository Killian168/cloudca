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
                "id": {"S": "killians-amazing-uuid"},
                "details": {
                    "M": {
                        "address": {"S": "killians-amazing-address"},
                        "birthdate": {"S": "killians-amazing-birthdate"},
                        "email": {"S": "killians-amazing-email"},
                        "family_name": {"S": "killians-amazing-family_name"},
                        "gender": {"S": "killians-amazing-gender"},
                        "given_name": {"S": "killians-amazing-given_name"},
                        "locale": {"S": "killians-amazing-locale"},
                        "role": {"S": "killians-amazing-role"},
                        "preferred_username": {"S": "killians-amazing-preferred_username"},
                    }
                },
                "manager": {"NULL": True},
                "officer": {"NULL": True},
                "academy_player": {"NULL": True},
                "player": {"NULL": True},
            },
        )

        # Call method
        response = get_all_members(None, None)
        print(f"response = {response}")

        # Assert Behaviour
        expected_response = {
            "statusCode": 200,
            "body": {
                "message": [
                    {
                        "id": "killians-amazing-uuid",
                        "details": {
                            "address": "killians-amazing-address",
                            "birthdate": "killians-amazing-birthdate",
                            "email": "killians-amazing-email",
                            "family_name": "killians-amazing-family_name",
                            "gender": "killians-amazing-gender",
                            "given_name": "killians-amazing-given_name",
                            "locale": "killians-amazing-locale",
                            "middle_name": None,
                            "name": None,
                            "nick_name": None,
                            "phone_number": None,
                            "picture": None,
                            "preferred_username": "killians-amazing-preferred_username",
                            "profile": None,
                            "updated_at": None,
                        },
                        "manager": None,
                        "officer": None,
                        "academy_player": None,
                        "player": None,
                    }
                ]
            },
        }
        self.assertEqual(response, expected_response)
