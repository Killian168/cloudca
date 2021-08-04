from enum import Enum
from json import dumps


class LambdaResponseCodes(Enum):
    """ Enum class that defines what HTTP response codes are valid, complying with standard
        HTTP best practises. """
    OK: int = 200
    BAD_REQUEST: int = 400


class Lambda:
    """ Class that represents an AWS Lambda """
    KEY_STATUS_CODE: str = "statusCode"
    KEY_BODY: str = "body"
    KEY_ERROR_MESSAGE: str = "errorMessage"
    KEY_MESSAGE: str = "message"

    @staticmethod
    def format_response(status_code: LambdaResponseCodes, response_message: str = None, error_message: str = None):
        """ Method that formats the return json for an AWS Lambda.
        
        Parameters
        ----------
        status_code : LambdaResponseCodes
            The HTTP status code to use in the AWS Lambda response.
        response_message : str
            The message to use in the AWS Lambda response under the key "message"
        error_message : str
            The message to use in the AWS Lambda response under the key "errorMessage"

        Returns
        -------
        return_json : dict
            The formatted response json to return from an AWS Lambda.
        """
        if error_message:
            return {
                Lambda.KEY_STATUS_CODE: status_code.value,
                Lambda.KEY_BODY: {Lambda.KEY_ERROR_MESSAGE: dumps(error_message)},
            }

        else:
            return {
                Lambda.KEY_STATUS_CODE: status_code.value,
                Lambda.KEY_BODY: {Lambda.KEY_MESSAGE: dumps(response_message)},
            }
