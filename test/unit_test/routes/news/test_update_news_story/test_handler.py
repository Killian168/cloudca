from test.unit_test.base_test_case import BaseTestCase
from test.test_fixtures.api_gateway_fixtures import APIGatewayFixtures
from test.test_fixtures.dynamo_fixtures import DynamoDbFixtures
from test.test_fixtures.fixtures import Fixtures

from parameterized import parameterized

from src.common.constants import NEWS_STORIES_TABLE_NAME, NEWS_THUMBNAILS_KEY, S3_BUCKET_NAME
from src.common.enums.api_response_codes import APIResponseCodes
from src.common.services.lambda_ import Lambda
from src.routes.news.update_news_story.handler import update_news_story


class TestUpdateNewsStoryHandler(BaseTestCase):
    @classmethod
    def setUpClass(cls, *args, **kwargs):
        super().setUpClass(dynamo_tables=[NEWS_STORIES_TABLE_NAME], s3_buckets=[S3_BUCKET_NAME])

    def test_should_return_200_and_update_news_story_metadata(self):
        # Set Up
        test_id = "killians-indecipherable-id"
        test_thumbnail_key = f"{NEWS_THUMBNAILS_KEY}/{test_id}.txt"
        self.dynamodb_client.put_item(
            TableName=NEWS_STORIES_TABLE_NAME,
            Item=DynamoDbFixtures.get_news_story_dynamodb_json(test_id, test_thumbnail_key),
        )
        self.s3_client.put_object(
            Body=Fixtures.get_base64_sample_pic(),
            Bucket=S3_BUCKET_NAME,
            Key=test_thumbnail_key,
        )

        # Call method
        event = {
            "story": {
                "id": test_id,
                "category": ["killians-cool-category"],
                "title": "killians-terrible-title",
                "description": "killians-different-description",
            }
        }
        request = APIGatewayFixtures.get_api_event(event)
        request["isBase64Encoded"] = True
        response = update_news_story(request, None)

        # Assert behaviour
        expected_response = Lambda.format_response(
            status_code=APIResponseCodes.OK, response_message=event.get("story")
        )
        self.assertEqual(response, expected_response)

        expected_dynamodb_entry = event.get("story")
        expected_dynamodb_entry["thumbnail_key"] = test_thumbnail_key
        self.assertEqual(
            Fixtures.get_dynamo_entry_news_story_json(test_id, test_thumbnail_key),
            expected_dynamodb_entry,
        )

    def test_should_return_200_and_update_news_story_thumbnail(self):
        # Set Up
        test_id = "killians-indecipherable-id"
        test_thumbnail_key = f"{NEWS_THUMBNAILS_KEY}/{test_id}.txt"
        self.dynamodb_client.put_item(
            TableName=NEWS_STORIES_TABLE_NAME,
            Item=DynamoDbFixtures.get_news_story_dynamodb_json(test_id, test_thumbnail_key),
        )
        self.s3_client.put_object(
            Body=Fixtures.get_base64_sample_pic(),
            Bucket=S3_BUCKET_NAME,
            Key=test_thumbnail_key,
        )

        # Call method
        event = {
            "story": {
                "id": test_id,
                "category": ["killians-cool-category"],
                "title": "killians-terrible-title",
                "description": "killians-different-description",
                "thumbnail": Fixtures.get_base64_sample_pic("test_image_1.png"),
            }
        }
        request = APIGatewayFixtures.get_api_event(event)
        request["isBase64Encoded"] = True
        response = update_news_story(request, None)

        # Assert behaviour
        expected_response = Lambda.format_response(
            status_code=APIResponseCodes.OK,
            response_message={
                "id": test_id,
                "category": ["killians-cool-category"],
                "title": "killians-terrible-title",
                "description": "killians-different-description",
                "thumbnail": Fixtures.get_base64_sample_pic("test_image_1.png"),
            },
        )
        self.assertEqual(response, expected_response)

    @parameterized.expand(
        [
            (
                "Missing Story",
                {"thumbnail": Fixtures.get_base64_sample_pic()},
                True,
                "Event processed does not have keys: story",
            ),
            (
                "Empty Event",
                {},
                False,
                "Event processed does not have keys: story",
            ),
            (
                "Should be 64 encoded",
                {
                    "story": {
                        "id": "killians-indecipherable-id",
                        "category": ["killians-cool-category"],
                        "title": "killians-terrible-title",
                        "description": "killians-different-description",
                        "thumbnail": Fixtures.get_base64_sample_pic("test_image_1.png"),
                    }
                },
                False,
                "is64Encoded is missing or false",
            ),
        ]
    )
    def test_should_return_400_and_error_message_on_bad_request(
        self, name, event, is_64_encoded, error_message
    ):
        # Call method
        request = APIGatewayFixtures.get_api_event(event)
        request["isBase64Encoded"] = is_64_encoded
        response = update_news_story(request, None)

        # Assert Behaviour
        expected_response = Lambda.format_response(
            status_code=APIResponseCodes.BAD_REQUEST, error_message=error_message
        )
        self.assertEqual(response, expected_response)

        response = self.dynamodb_client.scan(TableName=NEWS_STORIES_TABLE_NAME)
        self.assertEqual(len(response["Items"]), 0)
