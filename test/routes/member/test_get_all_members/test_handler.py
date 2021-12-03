from test.base_test_case import BaseTestCase
from test.test_fixtures.dynamo_fixtures import DynamoDbFixtures
from test.test_fixtures.fixtures import Fixtures

from src.common.constants import MEMBERS_TABLE_NAME
from src.common.enums.api_response_codes import APIResponseCodes
from src.common.services.lambda_ import Lambda
from src.routes.member.get_all_members.handler import get_all_members


class TestGetAllMembersHandler(BaseTestCase):
    @classmethod
    def setUpClass(cls, *args, **kwargs):
        super().setUpClass(dynamo_tables=[MEMBERS_TABLE_NAME])

    def test_should_return_200_and_members_list(self):
        # Set up
        member_id = "test_member_id"
        self.dynamodb_client.put_item(
            TableName=MEMBERS_TABLE_NAME,
            Item=DynamoDbFixtures.get_member_no_role_dynamo_json(member_id),
        )

        # Call method
        response = get_all_members(None, None)

        # Assert Behaviour
        expected_response = Lambda.format_response(
            status_code=APIResponseCodes.OK,
            response_message=[Fixtures.get_member_no_role_json(member_id)],
        )
        self.assertEqual(response, expected_response)
