import json

import boto3

from src.common.constants import NEWS_STORIES_TABLE_NAME, NEWS_THUMBNAILS_KEY, S3_BUCKET_NAME
from src.common.enums.api_response_codes import APIResponseCodes
from src.common.services.dynamodb import DynamoDB
from src.common.services.lambda_ import Lambda
from src.common.services.logger import get_logger

LOGGER = get_logger()


def delete_news_stories(event, context):
    body = json.loads(event.get("body", None))
    ids = body.get("ids", None)
    LOGGER.debug(f"ids passed in event is: {ids}")

    if ids is None:
        error_message = "Event processed contains invalid ids"
        LOGGER.error(error_message)
        return Lambda.format_response(
            status_code=APIResponseCodes.BAD_REQUEST, error_message=error_message
        )

    # Remove stories from news story table
    dynamo = DynamoDB(logger=LOGGER)
    dynamo.batch_delete(table_name=NEWS_STORIES_TABLE_NAME, ids=ids)

    # Remove any attached data from s3
    s3 = boto3.resource("s3")
    news_story_keys = [
        {"Key": f"{NEWS_THUMBNAILS_KEY}/{news_story_id}.txt"} for news_story_id in ids
    ]
    s3.meta.client.delete_objects(Bucket=S3_BUCKET_NAME, Delete={"Objects": news_story_keys})

    return Lambda.format_response(
        status_code=APIResponseCodes.OK,
        response_message=f"Successfully deleted news story with ids: {ids}",
    )
