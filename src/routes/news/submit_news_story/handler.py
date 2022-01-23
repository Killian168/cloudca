import json

import boto3

from src.common.constants import NEWS_STORIES_TABLE_NAME, S3_BUCKET_NAME
from src.common.enums.api_response_codes import APIResponseCodes
from src.common.models.news_story import NewsStory
from src.common.services.dynamodb import DynamoDB
from src.common.services.lambda_ import Lambda
from src.common.services.logger import get_logger

LOGGER = get_logger()


def submit_news_story(event, context):
    body = json.loads(event.get("body", None))

    story = body.get("story", None)
    is_64_encoded = event.get("is64Encoded", None)
    thumbnail = body.get("thumbnail", None)

    if story is None or is_64_encoded is None or thumbnail is None:
        missing_keys = []
        if story is None:
            missing_keys.append("story")
        if is_64_encoded is None:
            missing_keys.append("is64Encoded")
        if thumbnail is None:
            missing_keys.append("thumbnail")

        error_message = f"Event processed does not have keys: {missing_keys}"

        LOGGER.error(error_message)
        return Lambda.format_response(
            status_code=APIResponseCodes.BAD_REQUEST, error_message=error_message
        )

    news_story = NewsStory(**story)

    s3 = boto3.resource("s3")
    image_object = s3.Object(bucket_name=S3_BUCKET_NAME, key=news_story.thumbnail_key)
    image_object.put(Body=thumbnail)

    dynamo = DynamoDB(logger=LOGGER)
    dynamo.put_item(table_name=NEWS_STORIES_TABLE_NAME, item=news_story.dict())

    story = news_story.dict()
    del story["thumbnail_key"]
    story.update({"thumbnail": thumbnail})

    return Lambda.format_response(status_code=APIResponseCodes.OK, response_message=story)
