import json

import boto3

from src.common.constants import NEWS_STORIES_TABLE_NAME, S3_BUCKET_NAME
from src.common.enums.api_response_codes import APIResponseCodes
from src.common.models.news_story import NewsStory
from src.common.services.dynamodb import DynamoDB, UpdateError
from src.common.services.lambda_ import Lambda
from src.common.services.logger import get_logger

LOGGER = get_logger()


def update_news_story(event, context):
    body = json.loads(event.get("body", None))
    story = body.get("story", None)
    is_64_encoded = event.get("isBase64Encoded", None)

    if story is None:
        error_message = "Event processed does not have keys: story"
        LOGGER.error(error_message)
        return Lambda.format_response(
            status_code=APIResponseCodes.BAD_REQUEST, error_message=error_message
        )

    thumbnail = story.get("thumbnail", None)

    # Only the story metadata is changing, not the picture
    if thumbnail is None:
        news_story = NewsStory(**story)

        dynamodb = DynamoDB(logger=LOGGER)
        try:
            dynamodb.update_item(table_name=NEWS_STORIES_TABLE_NAME, item=news_story.dict())
        except UpdateError as e:
            return Lambda.format_response(
                status_code=APIResponseCodes.BAD_REQUEST, error_message=str(e)
            )

        return Lambda.format_response(status_code=APIResponseCodes.OK, response_message=story)

    # Picture needs to be updated as well
    else:
        if is_64_encoded is None or is_64_encoded is False:
            error_message = "is64Encoded is missing or false"
            LOGGER.error(error_message)
            return Lambda.format_response(
                status_code=APIResponseCodes.BAD_REQUEST, error_message=error_message
            )

        news_story = NewsStory(**story)

        s3 = boto3.resource("s3")
        image_object = s3.Object(bucket_name=S3_BUCKET_NAME, key=news_story.thumbnail_key)
        image_object.put(Body=thumbnail)

        dynamodb = DynamoDB(logger=LOGGER)
        try:
            dynamodb.update_item(table_name=NEWS_STORIES_TABLE_NAME, item=news_story.dict())
        except UpdateError as e:
            return Lambda.format_response(
                status_code=APIResponseCodes.BAD_REQUEST, error_message=str(e)
            )

        story = news_story.dict()
        del story["thumbnail_key"]
        story.update({"thumbnail": thumbnail})

        return Lambda.format_response(status_code=APIResponseCodes.OK, response_message=story)
