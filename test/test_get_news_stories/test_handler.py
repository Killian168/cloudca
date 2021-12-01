from test.base_test_case import BaseTestCase
from test.test_fixtures.dynamo_fixtures import DynamoDbFixtures
from test.test_fixtures.fixtures import Fixtures

from src.common.constants import NEWS_STORIES_TABLE_NAME, S3_BUCKET_NAME
from src.common.enums.api_response_codes import APIResponseCodes
from src.common.services.lambda_ import Lambda
from src.get_news_stories.handler import get_news_stories


class TestGetMembersByTeamHandler(BaseTestCase):
    @classmethod
    def setUpClass(cls, *args, **kwargs):
        super().setUpClass(dynamo_tables=[NEWS_STORIES_TABLE_NAME], s3_buckets=[S3_BUCKET_NAME])

    def test_should_return_200_and_members_list(self):
        # Set up
        story_id = "killians-indecipherable-id"
        bucket_key = "killians-key-kebab"

        self.dynamodb_client.put_item(
            TableName=NEWS_STORIES_TABLE_NAME,
            Item=DynamoDbFixtures.get_news_story_dynamodb_json(story_id, bucket_key),
        )
        self.s3_client.put_object(
            Body=Fixtures.get_base64_sample_pic(),
            Bucket=S3_BUCKET_NAME,
            Key=bucket_key,
        )

        # Call method
        response = get_news_stories({"category": "all"}, None)

        # Assert Behaviour
        expected_response = Lambda.format_response(
            status_code=APIResponseCodes.OK,
            response_message=[Fixtures.get_news_story_json(story_id)],
        )
        self.assertDictEqual(response, expected_response)

    def test_should_return_400_and_error_message_on_bad_request(self):
        response = get_news_stories({}, None)

        # Assert Behaviour
        expected_response = Lambda.format_response(
            status_code=APIResponseCodes.BAD_REQUEST,
            error_message="Event processed contains invalid category",
        )
        self.assertEqual(response, expected_response)
