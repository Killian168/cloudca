import json


class APIGatewayFixtures:
    @staticmethod
    def get_api_event(body=None):
        if body is None:
            body = {}
        if not isinstance(body, dict):
            raise ValueError

        user_agent = "PostmanRuntime/7.28.4"
        host = "mock-host"
        resource = "mock-resource"
        return {
            "message": None,
            "resource": resource,
            "path": resource,
            "httpMethod": "POST",
            "headers": {
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br",
                "CloudFront-Forwarded-Proto": "https",
                "CloudFront-Is-Desktop-Viewer": "true",
                "CloudFront-Is-Mobile-Viewer": "false",
                "CloudFront-Is-SmartTV-Viewer": "false",
                "CloudFront-Is-Tablet-Viewer": "false",
                "CloudFront-Viewer-Country": "IE",
                "Content-Type": "application/json",
                "Host": host,
                "User-Agent": user_agent,
                "X-Forwarded-Proto": "https",
            },
            "multiValueHeaders": {
                "Accept": ["*/*"],
                "Accept-Encoding": ["gzip, deflate, br"],
                "CloudFront-Forwarded-Proto": ["https"],
                "CloudFront-Is-Desktop-Viewer": ["true"],
                "CloudFront-Is-Mobile-Viewer": ["false"],
                "CloudFront-Is-SmartTV-Viewer": ["false"],
                "CloudFront-Is-Tablet-Viewer": ["false"],
                "CloudFront-Viewer-Country": ["IE"],
                "Content-Type": ["application/json"],
                "Host": [host],
                "User-Agent": [user_agent],
                "X-Forwarded-Proto": ["https"],
            },
            "queryStringParameters": None,
            "multiValueQueryStringParameters": None,
            "pathParameters": None,
            "stageVariables": None,
            "requestContext": {
                "resourcePath": resource,
                "httpMethod": "POST",
                "protocol": "HTTP/1.1",
                "requestTimeEpoch": 1642717058418,
                "identity": {
                    "cognitoIdentityPoolId": None,
                    "accountId": None,
                    "cognitoIdentityId": None,
                    "caller": None,
                    "sourceIp": "78.19.217.121",
                    "principalOrgId": None,
                    "accessKey": None,
                    "cognitoAuthenticationType": None,
                    "cognitoAuthenticationProvider": None,
                    "userArn": None,
                    "userAgent": user_agent,
                    "user": None,
                },
                "domainName": host,
            },
            "body": json.dumps(body),
            "isBase64Encoded": False,
        }
