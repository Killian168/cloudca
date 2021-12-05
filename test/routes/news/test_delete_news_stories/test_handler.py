from test.base_test_case import BaseTestCase
from test.test_fixtures.dynamo_fixtures import DynamoDbFixtures

from botocore.errorfactory import ClientError

from src.common.constants import NEWS_STORIES_TABLE_NAME, NEWS_THUMBNAILS_KEY, S3_BUCKET_NAME
from src.common.enums.api_response_codes import APIResponseCodes
from src.common.services.lambda_ import Lambda
from src.routes.news.delete_news_stories.handler import delete_news_stories


class TestGetMembersByTeamHandler(BaseTestCase):
    @classmethod
    def setUpClass(cls, *args, **kwargs):
        super().setUpClass(dynamo_tables=[NEWS_STORIES_TABLE_NAME], s3_buckets=[S3_BUCKET_NAME])

    def test_should_return_200_and_delete_one_item(self):
        # Set up
        test_story_id = "test_id"
        test_key = f"{NEWS_THUMBNAILS_KEY}/{test_story_id}.txt"
        ids = [test_story_id]
        self.dynamodb_client.put_item(
            TableName=NEWS_STORIES_TABLE_NAME,
            Item=DynamoDbFixtures.get_news_story_dynamodb_json(test_story_id, test_key),
        )

        # Call method
        response = delete_news_stories({"ids": ids}, None)

        # Assert behaviour
        expected_response = Lambda.format_response(
            status_code=APIResponseCodes.OK,
            response_message=f"Successfully deleted news story with ids: {ids}",
        )
        self.assertEqual(response, expected_response)

        with self.assertRaises(KeyError):
            _ = self.dynamodb_client.get_item(
                TableName=NEWS_STORIES_TABLE_NAME,
                Key={
                    "id": {
                        "S": ids[0],
                    }
                },
            )["Item"]

        with self.assertRaises(ClientError):
            _ = self.s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=test_key)

    def test_should_return_200_and_delete_multiple_items(self):
        # Set up
        test_story_id_1 = "test_id_1"
        test_story_id_2 = "test_id_2"
        test_key_1 = f"{NEWS_THUMBNAILS_KEY}/{test_story_id_1}.txt"
        test_key_2 = f"{NEWS_THUMBNAILS_KEY}/{test_story_id_2}.txt"
        ids = [test_story_id_1, test_story_id_2]
        self.dynamodb_client.put_item(
            TableName=NEWS_STORIES_TABLE_NAME,
            Item=DynamoDbFixtures.get_news_story_dynamodb_json(test_story_id_1, test_key_1),
        )
        self.dynamodb_client.put_item(
            TableName=NEWS_STORIES_TABLE_NAME,
            Item=DynamoDbFixtures.get_news_story_dynamodb_json(test_story_id_2, test_key_2),
        )

        # Call method
        response = delete_news_stories({"ids": ids}, None)

        # Assert behaviour
        expected_response = Lambda.format_response(
            status_code=APIResponseCodes.OK,
            response_message=f"Successfully deleted news story with ids: {ids}",
        )
        self.assertEqual(response, expected_response)

        with self.assertRaises(KeyError):
            _ = self.dynamodb_client.get_item(
                TableName=NEWS_STORIES_TABLE_NAME,
                Key={
                    "id": {
                        "S": test_story_id_1,
                    }
                },
            )["Item"]

        with self.assertRaises(ClientError):
            _ = self.s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=test_key_1)

        with self.assertRaises(KeyError):
            _ = self.dynamodb_client.get_item(
                TableName=NEWS_STORIES_TABLE_NAME,
                Key={
                    "id": {
                        "S": test_story_id_2,
                    }
                },
            )["Item"]

        with self.assertRaises(ClientError):
            _ = self.s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=test_key_2)

    def test_should_return_400_and_error_message_on_bad_request(self):
        response = delete_news_stories({}, None)

        # Assert Behaviour
        expected_response = Lambda.format_response(
            status_code=APIResponseCodes.BAD_REQUEST,
            error_message="Event processed contains invalid ids",
        )
        self.assertEqual(response, expected_response)
