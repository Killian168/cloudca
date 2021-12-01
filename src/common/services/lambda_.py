from json import dumps

from ..enums.api_response_codes import APIResponseCodes


class InvalidResponse(Exception):
    pass


class Lambda:
    KEY_STATUS_CODE = "statusCode"
    KEY_BODY = "body"
    KEY_HEADERS = "headers"
    KEY_64ENCODED = "isBase64Encoded"

    @staticmethod
    def _lambda_response_contract(
        status_code=None, headers=None, body=None, is_base_64_encoded=False
    ):
        if headers is None:
            headers = {}
        if status_code is None:
            raise InvalidResponse("status_code can not be None")
        if body is None:
            raise InvalidResponse("body can not be None")

        return {
            Lambda.KEY_STATUS_CODE: status_code,
            Lambda.KEY_HEADERS: headers,
            Lambda.KEY_BODY: dumps(body),
            Lambda.KEY_64ENCODED: is_base_64_encoded,
        }

    @staticmethod
    def format_response(status_code: APIResponseCodes, response_message=None, error_message=None):
        if error_message:
            return Lambda._lambda_response_contract(
                status_code=status_code.value, body={"errorMessage": error_message}
            )

        else:
            return Lambda._lambda_response_contract(
                status_code=status_code.value, body={"message": response_message}
            )
