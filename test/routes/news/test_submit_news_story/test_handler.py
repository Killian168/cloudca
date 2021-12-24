from test.base_test_case import BaseTestCase
from test.test_fixtures.fixtures import Fixtures
from unittest.mock import Mock

from parameterized import parameterized

import src.common.models.news_story
from src.common.constants import NEWS_STORIES_TABLE_NAME, S3_BUCKET_NAME
from src.common.enums.api_response_codes import APIResponseCodes
from src.common.services.lambda_ import Lambda
from src.routes.news.submit_news_story.handler import submit_news_story


class TestSubmitNewsStoryHandler(BaseTestCase):
    @classmethod
    def setUpClass(cls, *args, **kwargs):
        super().setUpClass(dynamo_tables=[NEWS_STORIES_TABLE_NAME], s3_buckets=[S3_BUCKET_NAME])

    def test_should_return_200_and_news_story(self):
        # Set Up
        test_id = "killians-indecipherable-id"
        src.common.models.news_story.uuid4 = Mock(return_value=test_id)
        test_event = {
            "story": {
                "category": ["killians-cool-category"],
                "title": "killians-terrible-title",
                "description": "killians-deceptive-description",
            },
            "thumbnail": Fixtures.get_base64_sample_pic(),
            "is64Encoded": True,
        }

        # Call method
        response = submit_news_story(test_event, None)

        # Assert Behaviour
        expected_response = Lambda.format_response(
            status_code=APIResponseCodes.OK, response_message=Fixtures.get_news_story_json(test_id)
        )
        self.assertEqual(response, expected_response)

        response = self.dynamodb_client.scan(
            TableName=NEWS_STORIES_TABLE_NAME,
            ExpressionAttributeValues={
                ":id": {
                    "S": test_id,
                },
            },
            FilterExpression="id = :id",
        )
        self.assertEqual(len(response["Items"]), 1)

    @parameterized.expand(
        [
            (
                "Missing Story",
                {"thumbnail": Fixtures.get_base64_sample_pic(), "is64Encoded": True},
                "Event processed does not have keys: ['story']",
            ),
            (
                "Empty Event",
                {},
                "Event processed does not have keys: ['story', 'is64Encoded', 'thumbnail']",
            ),
            (
                "Empty Event",
                {
                    "story": {
                        "category": ["killians-cool-category"],
                        "title": "killians-terrible-title",
                        "description": "killians-deceptive-description",
                    },
                    "thumbnail": Fixtures.get_base64_sample_pic(),
                },
                "Event processed does not have keys: ['is64Encoded']",
            ),
            (
                "TeamId is None",
                {
                    "story": {
                        "category": ["killians-cool-category"],
                        "title": "killians-terrible-title",
                        "description": "killians-deceptive-description",
                    },
                    "is64Encoded": True,
                },
                "Event processed does not have keys: ['thumbnail']",
            ),
        ]
    )
    def test_should_return_400_and_error_message_on_bad_request(self, name, event, error_message):
        # Call method
        response = submit_news_story(event, None)

        # Assert Behaviour
        expected_response = Lambda.format_response(
            status_code=APIResponseCodes.BAD_REQUEST, error_message=error_message
        )
        self.assertEqual(response, expected_response)

        response = self.dynamodb_client.scan(TableName=NEWS_STORIES_TABLE_NAME)
        self.assertEqual(len(response["Items"]), 0)
