import json

import boto3

from src.common.constants import NEWS_STORIES_TABLE_NAME, NEWS_THUMBNAILS_KEY, S3_BUCKET_NAME
from src.common.enums.api_response_codes import APIResponseCodes
from src.common.services.dynamodb import DeletionError, DynamoDB
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

    dynamo = DynamoDB(logger=LOGGER)

    ids_not_deleted = []
    for id in ids:
        try:
            dynamo.delete_item(table_name=NEWS_STORIES_TABLE_NAME, id=id)
        except DeletionError:
            ids_not_deleted.append(id)

        s3 = boto3.client("s3")
        s3.delete_object(Bucket=S3_BUCKET_NAME, Key=f"{NEWS_THUMBNAILS_KEY}/{id}.txt")

    if len(ids_not_deleted) > 0:
        return Lambda.format_response(
            status_code=APIResponseCodes.PARTIAL_SUCCESS, response_message={"ids": ids_not_deleted}
        )
    else:
        return Lambda.format_response(
            status_code=APIResponseCodes.OK,
            response_message=f"Successfully deleted news story with ids: {ids}",
        )
