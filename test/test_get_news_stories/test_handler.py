from test.test_fixtures.dynamo_fixtures import DynamoDbFixtures
from test.test_fixtures.fixtures import Fixtures
from unittest import TestCase

import boto3
from moto import mock_dynamodb2, mock_s3

from src.common.constants import NEWS_STORIES_TABLE_NAME, S3_BUCKET_NAME
from src.get_news_stories.handler import get_news_stories


class TestHandlerBaseCase(TestCase):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()


class TestGetMembersByTeamHandler(TestHandlerBaseCase):
    @mock_dynamodb2
    @mock_s3
    def test_should_return_200_and_members_list(self):
        # Set up
        story_id = "killians-indecipherable-id"
        bucket_key = "killians-key-kebab"
        dynamodb_client = boto3.client("dynamodb")
        s3_client = boto3.client("s3")

        dynamodb_client.create_table(
            TableName=NEWS_STORIES_TABLE_NAME,
            KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
        )

        dynamodb_client.put_item(
            TableName=NEWS_STORIES_TABLE_NAME,
            Item=DynamoDbFixtures.get_news_story_dynamodb_json(story_id, bucket_key),
        )

        s3_client.create_bucket(
            Bucket=S3_BUCKET_NAME,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-1"},
        )
        s3_client.put_object(
            Body=Fixtures.get_base64_sample_pic(),
            Bucket=S3_BUCKET_NAME,
            Key=bucket_key,
        )

        # Call method
        response = get_news_stories({"category": "all"}, None)

        # Assert Behaviour
        expected_response = {
            "statusCode": 200,
            "body": {"message": [Fixtures.get_news_story_json(story_id)]},
        }
        self.assertEqual(response, expected_response)

    def test_should_return_400_and_error_message_on_bad_request(self):
        response = get_news_stories({}, None)

        # Assert Behaviour
        expected_response = {
            "statusCode": 400,
            "body": {"errorMessage": "Event processed contains invalid category"},
        }
        self.assertEqual(response, expected_response)
