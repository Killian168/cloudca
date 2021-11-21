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
            {"errorMessage": "Event processed does not have key `TeamId`."},
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
        # Put manager item in table
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
                "manager": {
                    "M": {
                        "teams": {"L": [{"S": test_team_id}]},
                        "favorite_formation": {"S": "killians-amazing-favorite_formation"},
                        "training_times": {"L": [{"S": "killians-amazing-training_time"}]},
                        "win_record": {"N": "0"},
                        "loss_record": {"N": "0"},
                        "match_times": {"L": [{"S": "killians-amazing-training_time"}]},
                        "achievements": {"L": [{"S": "killians-amazing-achievement"}]},
                    }
                },
                "officer": {"NULL": True},
                "academy_player": {"NULL": True},
                "player": {"NULL": True},
            },
        )

        # Put player item in table
        dynamodb_client.put_item(
            TableName=MEMBERS_TABLE,
            Item={
                "id": {"S": "killians-amazing-uuid-2"},
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
                "player": {"M": {"teams": {"L": [{"S": test_team_id}]}}},
            },
        )

        # Call method
        response = get_members_by_team(mock_event, None)

        # Assert Behaviour
        expected_response = {
            "body": {
                "message": [
                    {
                        "academy_player": None,
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
                        "id": "killians-amazing-uuid",
                        "manager": {
                            "achievements": ["killians-amazing-achievement"],
                            "favorite_formation": "killians-amazing-favorite_formation",
                            "loss_record": 0,
                            "match_times": ["killians-amazing-training_time"],
                            "teams": ["test-team"],
                            "training_times": ["killians-amazing-training_time"],
                            "win_record": 0,
                        },
                        "officer": None,
                        "player": None,
                    },
                    {
                        "academy_player": None,
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
                        "id": "killians-amazing-uuid-2",
                        "manager": None,
                        "officer": None,
                        "player": {
                            "achievements": [],
                            "all_time_appearances": 0,
                            "all_time_assists": 0,
                            "all_time_goals": 0,
                            "match_times": [],
                            "positions": [],
                            "season_appearances": 0,
                            "season_assists": 0,
                            "season_goals": 0,
                            "teams": ["test-team"],
                            "training_times": [],
                        },
                    },
                ]
            },
            "statusCode": 200,
        }
        self.assertEqual(response, expected_response)
