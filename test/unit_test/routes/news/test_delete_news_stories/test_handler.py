from test.unit_test.base_test_case import BaseTestCase
from test.test_fixtures.api_gateway_fixtures import APIGatewayFixtures
from test.test_fixtures.dynamo_fixtures import DynamoDbFixtures
from test.test_fixtures.fixtures import Fixtures

from botocore.errorfactory import ClientError
from parameterized import parameterized

from src.common.constants import NEWS_STORIES_TABLE_NAME, NEWS_THUMBNAILS_KEY, S3_BUCKET_NAME
from src.common.enums.api_response_codes import APIResponseCodes
from src.common.services.lambda_ import Lambda
from src.routes.news.delete_news_stories.handler import delete_news_stories


class TestDeleteNewsStoriesHandler(BaseTestCase):
    @classmethod
    def setUpClass(cls, *args, **kwargs):
        super().setUpClass(dynamo_tables=[NEWS_STORIES_TABLE_NAME], s3_buckets=[S3_BUCKET_NAME])

    @parameterized.expand(
        [
            (
                "Delete One Item",
                ["test_id"],
                "Successfully deleted news story with ids: ['test_id']",
            ),
            (
                "Delete Two Items",
                ["test_id_1", "test_id_2"],
                "Successfully deleted news story with ids: ['test_id_1', 'test_id_2']",
            ),
            (
                "Delete Three Items",
                ["test_id_1", "test_id_2", "test_id_3"],
                "Successfully deleted news story with ids: ['test_id_1', 'test_id_2', 'test_id_3']",
            ),
        ]
    )
    def test_should_return_200(self, name, ids, response_message):
        # Set up
        test_keys = [f"{NEWS_THUMBNAILS_KEY}/{id}.txt" for id in ids]

        for i in range(len(ids)):
            self.dynamodb_client.put_item(
                TableName=NEWS_STORIES_TABLE_NAME,
                Item=DynamoDbFixtures.get_news_story_dynamodb_json(ids[i], test_keys[i]),
            )

            self.s3_client.put_object(
                Body=Fixtures.get_base64_sample_pic(), Bucket=S3_BUCKET_NAME, Key=test_keys[i]
            )

        # Call method
        request = APIGatewayFixtures.get_api_event({"ids": ids})
        response = delete_news_stories(request, None)

        # Assert behaviour
        expected_response = Lambda.format_response(
            status_code=APIResponseCodes.OK,
            response_message=response_message,
        )
        self.assertEqual(response, expected_response)

        for id in ids:
            with self.assertRaises(KeyError):
                _ = self.dynamodb_client.get_item(
                    TableName=NEWS_STORIES_TABLE_NAME,
                    Key={
                        "id": {
                            "S": id,
                        }
                    },
                )["Item"]

        for test_key in test_keys:
            with self.assertRaises(ClientError):
                _ = self.s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=test_key)

    def test_should_return_200_and_delete_no_items_from_invalid_ids(self):
        # Set up
        team_id = "id"
        test_id = "Not an id"
        test_key = f"{NEWS_THUMBNAILS_KEY}/{team_id}.txt"

        self.dynamodb_client.put_item(
            TableName=NEWS_STORIES_TABLE_NAME,
            Item=DynamoDbFixtures.get_news_story_dynamodb_json(team_id, test_key),
        )

        self.s3_client.put_object(
            Body=Fixtures.get_base64_sample_pic(), Bucket=S3_BUCKET_NAME, Key=test_key
        )

        # Call method
        request = APIGatewayFixtures.get_api_event({"ids": [test_id]})
        response = delete_news_stories(request, None)

        # Assert behaviour
        expected_response = Lambda.format_response(
            status_code=APIResponseCodes.OK,
            response_message=f"Successfully deleted news story with ids: {[test_id]}",
        )
        self.assertEqual(response, expected_response)

        _ = self.dynamodb_client.get_item(
            TableName=NEWS_STORIES_TABLE_NAME,
            Key={
                "id": {
                    "S": team_id,
                }
            },
        )["Item"]

        _ = self.s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=test_key)

    @parameterized.expand(
        [
            (
                "Invalid ids Key",
                {"not correct ids": "Test"},
                "Event processed contains invalid ids",
            ),
            ("Empty Event", {}, "Event processed contains invalid ids"),
            ("ids is None", {"ids": None}, "Event processed contains invalid ids"),
        ]
    )
    def test_should_return_400_and_error_message_on_bad_request(self, name, event, error_message):
        request = APIGatewayFixtures.get_api_event(event)
        response = delete_news_stories(request, None)

        # Assert Behaviour
        expected_response = Lambda.format_response(
            status_code=APIResponseCodes.BAD_REQUEST,
            error_message=error_message,
        )
        self.assertEqual(response, expected_response)
