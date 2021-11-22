from ..enums.api_response_codes import APIResponseCodes


class Lambda:
    KEY_STATUS_CODE = "statusCode"
    KEY_BODY = "body"

    @staticmethod
    def format_response(status_code: APIResponseCodes, response_message=None, error_message=None):
        if error_message:
            return {
                Lambda.KEY_STATUS_CODE: status_code.value,
                Lambda.KEY_BODY: {"errorMessage": error_message},
            }

        else:
            return {
                Lambda.KEY_STATUS_CODE: status_code.value,
                Lambda.KEY_BODY: {"message": response_message},
            }
