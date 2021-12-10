from test.base_test_case import BaseTestCase
from test.test_fixtures.dynamo_fixtures import DynamoDbFixtures
from test.test_fixtures.fixtures import Fixtures

from parameterized import parameterized

from src.common.constants import MEMBERS_TABLE_NAME
from src.common.enums.api_response_codes import APIResponseCodes
from src.common.services.lambda_ import Lambda
from src.routes.member.update_member.handler import update_member


class TestUpdateMembersHandler(BaseTestCase):
    TEST_UUID = "16ba49bc-5464-4ee2-9846-77264b3ac62d"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def setUpClass(cls, *args, **kwargs):
        super().setUpClass(dynamo_tables=[MEMBERS_TABLE_NAME])

    def test_should_return_200_and_update_member(self):
        # Set up
        self.dynamodb_client.put_item(
            TableName=MEMBERS_TABLE_NAME,
            Item=DynamoDbFixtures.get_manager_dynamo_json(TestUpdateMembersHandler.TEST_UUID),
        )

        # Call method
        response = update_member(
            {"Member": Fixtures.get_member_no_role_json(TestUpdateMembersHandler.TEST_UUID)}, None
        )

        # Assert Behaviour
        expected_response = Lambda.format_response(
            status_code=APIResponseCodes.OK,
            response_message=Fixtures.get_member_no_role_json(TestUpdateMembersHandler.TEST_UUID),
        )
        self.assertEqual(response, expected_response)

    @parameterized.expand(
        [
            (
                "Empty Event",
                {},
                "Event processed does not have key `Member`.",
            ),
            (
                "Member is None",
                {"Member": None},
                "Member can not be: None",
            ),
            (
                "Missing Details",
                {"Member": {}},
                {"field required": ["details"]},
            ),
            (
                "Invalid Member",
                {"Member": {"details": {}}},
                {
                    "field required": [
                        {"details": "address"},
                        {"details": "birthdate"},
                        {"details": "email"},
                        {"details": "family_name"},
                        {"details": "gender"},
                        {"details": "given_name"},
                        {"details": "locale"},
                        {"details": "preferred_username"},
                    ]
                },
            ),
            (
                "Should not put entry in table",
                {"Member": Fixtures.get_member_no_role_json(TEST_UUID)},
                f"Error updating item with id:{TEST_UUID} in table Members, responded with: No item"
                f" with id {TEST_UUID} found",
            ),
        ]
    )
    def test_should_return_400_and_error_message_on_bad_request(self, name, event, error_message):
        # Call method
        response = update_member(event, None)

        # Assert Behaviour
        expected_response = Lambda.format_response(
            status_code=APIResponseCodes.BAD_REQUEST,
            error_message=error_message,
        )
        self.assertEqual(response, expected_response)