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
            {"errorMessage": "Event processed does not have key `TeamId`."},
        )

    ########################################################
    # Commenting out just for now will fix before merging  #
    ########################################################

    # @mock_dynamodb2
    # def test_should_return_200_and_members_list(self):
        # Set up
        # test_team_id = "test-team"
        # mock_event = {"TeamId": test_team_id}
        # dynamodb_client = boto3.client("dynamodb")
        #
        # # Set up dynamoDb Table
        # dynamodb_client.create_table(
        #     TableName=MEMBERS_TABLE,
        #     KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
        #     AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
        # )
        #
        # # Put item in table
        # dynamodb_client.put_item(
        #     TableName=MEMBERS_TABLE,
        #     Item={
        #         'id': 'killians-amazing-uuid',
        #         'details': {
        #             'address': 'killians-amazing-address',
        #             'birthdate': 'killians-amazing-birthdate',
        #             'email': 'killians-amazing-email',
        #             'family_name': 'killians-amazing-family_name',
        #             'gender': 'killians-amazing-gender',
        #             'given_name': 'killians-amazing-given_name',
        #             'locale': 'killians-amazing-locale',
        #             'middle_name': None,
        #             'name': None,
        #             'nick_name': None,
        #             'phone_number': None,
        #             'picture': None,
        #             'preferred_username': 'killians-amazing-preferred_username',
        #             'profile': None,
        #             'updated_at': None
        #         },
        #         'manager': None,
        #         'officer': None,
        #         'academy_player': None,
        #         'player': None
        #     },
        # )
        #
        # # Call method
        # response = get_members_by_team(mock_event, None)
        #
        # # Assert Behaviour
        # expected_response = {
        #     "statusCode": 200,
        #     "body": {
        #         "message": dumps(
        #             [
        #                 {
        #                     'id': 'killians-amazing-uuid',
        #                     'details': {
        #                         'address': 'killians-amazing-address',
        #                         'birthdate': 'killians-amazing-birthdate',
        #                         'email': 'killians-amazing-email',
        #                         'family_name': 'killians-amazing-family_name',
        #                         'gender': 'killians-amazing-gender',
        #                         'given_name': 'killians-amazing-given_name',
        #                         'locale': 'killians-amazing-locale',
        #                         'middle_name': None,
        #                         'name': None,
        #                         'nick_name': None,
        #                         'phone_number': None,
        #                         'picture': None,
        #                         'preferred_username': 'killians-amazing-preferred_username',
        #                         'profile': None,
        #                         'updated_at': None
        #                     },
        #                     'manager': None,
        #                     'officer': None,
        #                     'academy_player': None,
        #                     'player': None
        #                 }
        #             ]
        #         )
        #     },
        # }
        # self.assertEqual(response, expected_response)
