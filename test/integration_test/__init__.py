import os
import pytest

api_gateway_prefix = os.environ.get("API_GATEWAY_PREFIX")
aws_region = os.environ.get("AWS_DEFAULT_REGION")


@pytest.fixture
def get_api_url():
    def _method(resource, route):
        return f"https://{api_gateway_prefix}.execute-api.{aws_region}.amazonaws.com/dev/{resource}/{route}"

    return _method
