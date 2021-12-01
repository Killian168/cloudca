import logging
from unittest import TestCase

import boto3
from moto import mock_dynamodb2, mock_s3


class BaseTestCase(TestCase):
    """Base Class all tests inherit from.
    This class ensures that all resources are properly mocked and
    cleaned up.
    """

    dynamodb_mock = None
    s3_mock = None
    s3_client = None
    dynamodb_client = None
    should_log = None
    s3_buckets = None
    dynamo_tables = None

    @classmethod
    def setUpClass(cls, dynamo_tables=None, s3_buckets=None, should_log=False):
        cls.dynamo_tables = dynamo_tables
        cls.s3_buckets = s3_buckets
        cls.should_log = should_log

        cls._start_mocking()
        cls._set_up_boto3_clients()
        if cls.dynamo_tables is not None:
            cls._set_up_dynamodb_tables()

        if cls.s3_buckets is not None:
            cls._set_up_s3_buckets()

        if not cls.should_log:
            cls._disable_logging()

    @classmethod
    def tearDownClass(cls):
        if cls.dynamo_tables is not None:
            cls._delete_dynamodb_tables()

        if cls.s3_buckets is not None:
            cls._delete_s3_buckets()

        if not cls.should_log:
            # re-enables logging
            logging.disable(logging.NOTSET)
        cls._reset_boto3_clients()
        cls._stop_mocking()

    @classmethod
    def _set_up_dynamodb_tables(cls):
        for table_name in cls.dynamo_tables:
            cls.dynamodb_client.create_table(
                TableName=table_name,
                KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
                AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
            )

    @classmethod
    def _delete_dynamodb_tables(cls):
        for table_name in cls.dynamo_tables:
            cls.dynamodb_client.delete_table(TableName=table_name)

    @classmethod
    def _set_up_s3_buckets(cls):
        for bucket_name in cls.s3_buckets:
            cls.s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={"LocationConstraint": "eu-west-1"},
            )

    @classmethod
    def _delete_s3_buckets(cls):
        for bucket_name in cls.s3_buckets:
            bucket = boto3.resource("s3").Bucket(bucket_name)
            bucket.objects.all().delete()
            bucket.delete()

    @classmethod
    def _set_up_boto3_clients(cls):
        if cls.dynamo_tables is not None:
            cls.dynamodb_client = boto3.client("dynamodb")
        if cls.s3_buckets is not None:
            cls.s3_client = boto3.client("s3")

    @classmethod
    def _reset_boto3_clients(cls):
        if cls.dynamo_tables is not None:
            cls.dynamodb_client = None
        if cls.s3_buckets is not None:
            cls.s3_client = None

    @classmethod
    def _disable_logging(cls):
        logging.disable(logging.CRITICAL)
        logging.disable(logging.DEBUG)
        logging.disable(logging.INFO)
        logging.disable(logging.ERROR)

    @classmethod
    def _start_mocking(cls):
        cls.s3_mock = mock_s3()
        cls.dynamodb_mock = mock_dynamodb2()

        cls.s3_mock.start()
        cls.dynamodb_mock.start()

    @classmethod
    def _stop_mocking(cls):
        cls.s3_mock.stop()
        cls.dynamodb_mock.stop()

        cls.s3_mock = None
        cls.dynamodb_mock = None
