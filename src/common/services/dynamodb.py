import boto3
from boto3.dynamodb.conditions import Or

from ..services.logger import get_logger


class ScanningError(Exception):
    def __init__(self, table_name):
        super().__init__(f"Error scanning {table_name}")


class DynamoDB:
    def __init__(self, logger=None, dynamodb_resource=None):
        if logger is None:
            logger = get_logger()
        if dynamodb_resource is None:
            dynamodb_resource = boto3.resource("dynamodb")

        self.logger = logger
        self.dynamodb_resource = dynamodb_resource

    def scan_table(self, table_name, filter_expression):
        teams_table = self.dynamodb_resource.Table(table_name)
        response = teams_table.scan(FilterExpression=filter_expression)
        self.logger.debug(f"{table_name} Table scan responded with: {response}")
        if response["Items"]:
            return response["Items"]
        else:
            raise ScanningError(table_name)

    @staticmethod
    def create_or_filter_expression(conditions):
        if len(conditions) == 1 or len(conditions) == 2:
            if len(conditions) == 1:
                return conditions[0]
            else:
                return Or(conditions[0], conditions[1])

        else:
            middle_index = len(conditions) / 2
            left_arr = conditions[:middle_index]
            right_arr = conditions[middle_index + 1 :]  # noqa: E203
            return Or(
                DynamoDB.create_or_filter_expression(left_arr),
                DynamoDB.create_or_filter_expression(right_arr),
            )
