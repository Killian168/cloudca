from enum import Enum
from json import dumps


class LambdaResponseCodes(Enum):
    OK = 200
    BAD_REQUEST = 400


class Lambda:

    KEY_STATUS_CODE = 'statusCode'
    KEY_BODY = 'body'

    def __init__(self, my_var=None):
        self.my_var = my_var

    @staticmethod
    def format_response(status_code: LambdaResponseCodes, response_message=None, error_message=None):
        if error_message:
            return {
                Lambda.KEY_STATUS_CODE: status_code.value,
                Lambda.KEY_BODY: {
                    'errorMessage': dumps(error_message)
                }
            }

        else:
            return {
                Lambda.KEY_STATUS_CODE: status_code.value,
                Lambda.KEY_BODY: {
                    'message': dumps(response_message)
                }
            }