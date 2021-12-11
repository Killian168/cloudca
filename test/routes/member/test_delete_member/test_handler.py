from test.base_test_case import BaseTestCase
from test.test_fixtures.dynamo_fixtures import DynamoDbFixtures

from parameterized import parameterized

from src.common.constants import MEMBERS_TABLE_NAME
from src.common.enums.api_response_codes import APIResponseCodes
from src.common.services.lambda_ import Lambda
from src.routes.member.delete_member.handler import delete_member


class TestDeleteMembersHandler(BaseTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def setUpClass(cls, *args, **kwargs):
        super().setUpClass(dynamo_tables=[MEMBERS_TABLE_NAME])

    def test_should_return_200_and_delete_member(self):
        # Set up
        test_uuid = "16ba49bc-5464-4ee2-9846-77264b3ac62d"
        self.dynamodb_client.put_item(
            TableName=MEMBERS_TABLE_NAME,
            Item=DynamoDbFixtures.get_member_no_role_dynamo_json(test_uuid),
        )

        # Call method
        response = delete_member({"MemberId": test_uuid}, None)

        # Assert Behaviour
        expected_response = Lambda.format_response(
            status_code=APIResponseCodes.OK,
            response_message=f"Successfully deleted Member with id: {test_uuid}",
        )
        self.assertEqual(response, expected_response)

        response = self.dynamodb_client.scan(
            TableName=MEMBERS_TABLE_NAME,
            ExpressionAttributeValues={
                ":id": {
                    "S": test_uuid,
                },
            },
            FilterExpression="id = :id",
        )
        self.assertEqual(len(response["Items"]), 0)

    @parameterized.expand(
        [
            (
                "Empty Event",
                {},
                APIResponseCodes.BAD_REQUEST,
                "MemberId can not be: None",
            ),
            (
                "MemberId is None",
                {"MemberId": None},
                APIResponseCodes.BAD_REQUEST,
                "MemberId can not be: None",
            ),
        ]
    )
    def test_should_return_400_and_error_message_on_bad_request(
        self, name, event, status_code, error_message
    ):
        # Call method
        response = delete_member(event, None)

        # Assert Behaviour
        expected_response = Lambda.format_response(
            status_code=status_code,
            error_message=error_message,
        )
        self.assertEqual(response, expected_response)

    def test_should_return_20_for_no_id_found(self):
        # Call method
        response = delete_member({"MemberId": "not a valid id"}, None)

        # Assert Behaviour
        expected_response = Lambda.format_response(
            status_code=APIResponseCodes.OK,
            response_message="Successfully deleted Member with id: not a valid id",
        )
        self.assertEqual(response, expected_response)
