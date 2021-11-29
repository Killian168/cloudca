import boto3
from boto3.dynamodb.conditions import Attr

from src.common.constants import NEWS_STORIES_TABLE_NAME, S3_BUCKET_NAME
from src.common.enums.api_response_codes import APIResponseCodes
from src.common.enums.news_categories import NewsCategories
from src.common.models.news_story import NewsStory
from src.common.services.dynamodb import DynamoDB
from src.common.services.lambda_ import Lambda
from src.common.services.logger import get_logger

LOGGER = get_logger()


def get_news_stories(event, context):
    category = event.get("category", None)
    LOGGER.debug(f"category value passed in event is: {category}")

    if not NewsCategories.has_value(category):
        error_message = "Event processed contains invalid category"
        LOGGER.error(error_message)
        return Lambda.format_response(
            status_code=APIResponseCodes.BAD_REQUEST, error_message=error_message
        )

    dynamo = DynamoDB(logger=LOGGER)

    if category is NewsCategories.all:
        response = dynamo.scan_table(table_name=NEWS_STORIES_TABLE_NAME)
    else:
        response = dynamo.scan_table(
            table_name=NEWS_STORIES_TABLE_NAME,
            filter_expression=Attr("category").contains(category),
        )

    news_story_objs = [NewsStory(**obj) for obj in response]

    news_stories = []
    s3 = boto3.resource("s3")

    for news_story in news_story_objs:
        story = news_story.dict()
        thumbnail_uri = s3.Object(S3_BUCKET_NAME, news_story.thumbnail_key)
        thumbnail_base_64 = thumbnail_uri.get()["Body"].read().decode("utf-8")
        del story["thumbnail_key"]
        story.update({"thumbnail": thumbnail_base_64})
        news_stories.append(story)

    return Lambda.format_response(status_code=APIResponseCodes.OK, response_message=news_stories)
