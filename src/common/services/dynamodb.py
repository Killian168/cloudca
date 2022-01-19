import boto3
from boto3.dynamodb.conditions import Key, Or
from botocore.exceptions import ClientError

from ..services.logger import get_logger


class ScanningError(Exception):
    def __init__(self, table_name):
        super().__init__(f"Error scanning {table_name}")


class WriteError(Exception):
    def __init__(self, table_name, item, response):
        super().__init__(
            f"Error putting item:{item}, into table {table_name}, responded with: {response}"
        )


class DeletionError(Exception):
    def __init__(self, table_name, id, response):
        super().__init__(
            f"Error deleting item with id:{id} from table {table_name}, responded with: {response}"
        )


class UpdateError(Exception):
    def __init__(self, table_name, id, response):
        super().__init__(
            f"Error updating item with id:{id} in table {table_name}, responded with: {response}"
        )


class DynamoDB:
    def __init__(self, logger=None, dynamodb_resource=None):
        if logger is None:
            logger = get_logger()
        if dynamodb_resource is None:
            dynamodb_resource = boto3.resource("dynamodb")

        self.logger = logger
        self.dynamodb_resource = dynamodb_resource

    # Note: This might be a good candidate for numba
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

    @staticmethod
    def _get_update_params(body):
        update_expression = ["set "]
        update_names = dict()
        update_values = dict()

        for index, (key, val) in enumerate(body.items()):
            update_expression.append(f" #{key} = :{index}{key},")
            update_values[f":{index}{key}"] = val
            update_names[f"#{key}"] = key

        return "".join(update_expression)[:-1], update_names, update_values

    def scan_table(self, table_name, filter_expression=None):
        table = self.dynamodb_resource.Table(table_name)

        if filter_expression:
            response = table.scan(FilterExpression=filter_expression)
        else:
            response = table.scan()

        self.logger.debug(f"{table_name} Table scan responded with: {response}")

        if response["Items"]:
            return response["Items"]
        else:
            raise ScanningError(table_name)

    def put_item(self, table_name, item, conditions=None):
        table = self.dynamodb_resource.Table(table_name)
        if conditions is None:
            response = table.put_item(Item=item)
        else:
            response = table.put_item(Item=item, ConditionExpression=conditions)
        if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
            raise WriteError(table_name, item, response)

    def delete_item(self, table_name, id):
        table = self.dynamodb_resource.Table(table_name)
        response = table.delete_item(Key={"id": id})
        if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
            raise DeletionError(table_name, id, response)

    def update_item(self, table_name, item):
        table = self.dynamodb_resource.Table(table_name)
        item_id = item["id"]
        del item["id"]
        update_expressions, update_names, update_values = DynamoDB._get_update_params(item)

        try:
            response = table.update_item(
                Key={"id": item_id},
                UpdateExpression=update_expressions,
                ExpressionAttributeValues=dict(update_values),
                ExpressionAttributeNames=dict(update_names),
                ConditionExpression=Key("id").eq(item_id),
                ReturnValues="ALL_NEW",
            )
        except ClientError as e:
            if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
                raise UpdateError(table_name, item_id, f"No item with id {item_id} found")
            else:  # Re-raise exception if it's not of type ConditionalCheckFailedException
                raise e

        if response["Attributes"]:
            return response
        else:
            raise UpdateError(table_name, item_id, response)
