import logging
from unittest import TestCase
from src.common.constants import TEAM_TABLE_NAME, MEMBERS_TABLE_NAME, S3_BUCKET_NAME, NEWS_STORIES_TABLE_NAME
from moto import mock_dynamodb2, mock_s3

import boto3


@mock_dynamodb2
@mock_s3
class BaseTestCase(TestCase):
    """ Base Class all tests inherit from
        This class ensures that all resources are properly mocked and
        cleaned up.
    """

    def _set_up_dynamodb_tables(self):
        self.dynamodb_client.create_table(
            TableName=TEAM_TABLE_NAME,
            KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
        )
        self.dynamodb_client.create_table(
            TableName=MEMBERS_TABLE_NAME,
            KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
        )
        self.dynamodb_client.create_table(
            TableName=NEWS_STORIES_TABLE_NAME,
            KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
        )

    def _delete_dynamodb_tables(self):
        self.dynamodb_client.delete_table(
            TableName=TEAM_TABLE_NAME
        )
        self.dynamodb_client.delete_table(
            TableName=MEMBERS_TABLE_NAME
        )
        self.dynamodb_client.delete_table(
            TableName=NEWS_STORIES_TABLE_NAME
        )

    def _set_up_s3_buckets(self):
        self.s3_client.create_bucket(
            Bucket=S3_BUCKET_NAME,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-1"},
        )

    def _delete_s3_buckets(self):
        self._delete_s3_bucket(S3_BUCKET_NAME)

    def _delete_s3_bucket(self, bucket_name):
        bucket = boto3.resource('s3').Bucket(bucket_name)
        bucket.objects.all().delete()
        bucket.delete()

    def _set_up_boto3_clients(self):
        self.dynamodb_client = boto3.client('dynamodb')
        self.s3_client = boto3.client('s3')

    def _reset_boto3_clients(self):
        self.dynamodb_client = None
        self.s3_client = None

    def _disable_logging(self):
        logging.disable(logging.CRITICAL)
        logging.disable(logging.DEBUG)
        logging.disable(logging.INFO)
        logging.disable(logging.ERROR)

    def setUp(self):
        self._set_up_boto3_clients()
        self._set_up_dynamodb_tables()
        self._set_up_s3_buckets()
        self._disable_logging()
        super().setUp()

    def tearDown(self):
        self._delete_dynamodb_tables()
        self._delete_s3_buckets()
        self._reset_boto3_clients()
        logging.disable(logging.NOTSET)
        super().tearDown()
