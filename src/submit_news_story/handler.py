import boto3

from src.common.constants import NEWS_STORIES_TABLE_NAME, S3_BUCKET_NAME
from src.common.enums.api_response_codes import APIResponseCodes
from src.common.models.news_story import NewsStory
from src.common.services.dynamodb import DynamoDB
from src.common.services.lambda_ import Lambda
from src.common.services.logger import get_logger

LOGGER = get_logger()


def submit_news_story(event, context):
    try:
        story = event["story"]
        LOGGER.debug(f"story value passed in event is: {story}")
    except KeyError:
        error_message = "Event processed does not have key `story`."
        LOGGER.error(error_message)
        return Lambda.format_response(
            status_code=APIResponseCodes.BAD_REQUEST, error_message=error_message
        )

    try:
        is_64_encoded = event["is64Encoded"]
        LOGGER.debug(f"story value passed in event is: {is_64_encoded}")
    except KeyError:
        error_message = "Event processed does not have key `is64Encoded`."
        LOGGER.error(error_message)
        return Lambda.format_response(
            status_code=APIResponseCodes.BAD_REQUEST, error_message=error_message
        )

    try:
        thumbnail = event["thumbnail"]
        LOGGER.debug(f"story value passed in event is: {thumbnail}")
    except KeyError:
        error_message = "Event processed does not have key `thumbnail`."
        LOGGER.error(error_message)
        return Lambda.format_response(
            status_code=APIResponseCodes.BAD_REQUEST, error_message=error_message
        )

    thumbnail = thumbnail.decode("utf-8")

    news_story = NewsStory(**story)

    s3 = boto3.resource("s3")
    image_object = s3.Object(bucket_name=S3_BUCKET_NAME, key=news_story.thumbnail_key)
    image_object.put(Body=thumbnail)

    dynamo = DynamoDB()
    dynamo.put_item(table_name=NEWS_STORIES_TABLE_NAME, item=news_story.dict())

    story = news_story.dict()
    del story["thumbnail_key"]
    story.update({"thumbnail": thumbnail})

    return Lambda.format_response(status_code=APIResponseCodes.OK, response_message=story)
