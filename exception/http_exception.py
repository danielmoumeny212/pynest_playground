from typing import Any, Dict, Optional, Union

class HttpException(Exception):
    """
    Defines the base HTTP exception, which can be handled by a custom exception handler.
    """

    def __init__(self, response: Union[str, Dict[str, Any]], status: int, options: Optional[Dict[str, Any]] = None):
        """
        Instantiate a plain HTTP Exception.

        :param response: string, object describing the error condition or the error cause.
        :param status: HTTP response status code.
        :param options: An object used to add an error cause.
        """
        super().__init__()
        self.response = response
        self.status = status
        self.options = options or {}
        self.cause = self.options.get('cause')
        self.message = self.init_message()
        self.name = self.__class__.__name__

    def init_message(self) -> str:
        if isinstance(self.response, str):
            return self.response
        elif isinstance(self.response, dict) and 'message' in self.response and isinstance(self.response['message'], str):
            return self.response['message']
        else:
            return ' '.join([word for word in self.__class__.__name__.split('_')]) or 'Error'

    def get_response(self) -> Union[str, Dict[str, Any]]:
        return self.response

    def get_status(self) -> int:
        return self.status

    @staticmethod
    def create_body(message: Optional[Union[str, Dict[str, Any]]] = None, error: Optional[str] = None, status_code: Optional[int] = None) -> Dict[str, Any]:
        if message is None:
            return {
                'message': error,
                'status_code': status_code,
            }

        if isinstance(message, (str, list)):
            return {
                'message': message,
                'error': error,
                'status_code': status_code,
            }

        return message

    @staticmethod
    def get_description_from(description_or_options: Union[str, Dict[str, Any]]) -> str:
        return description_or_options if isinstance(description_or_options, str) else description_or_options.get('description', '')

    @staticmethod
    def get_http_exception_options_from(description_or_options: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
        return {} if isinstance(description_or_options, str) else description_or_options

    @staticmethod
    def extract_description_and_options_from(description_or_options: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
        description = description_or_options if isinstance(description_or_options, str) else description_or_options.get('description', '')
        http_exception_options = {} if isinstance(description_or_options, str) else description_or_options
        return {
            'description': description,
            'http_exception_options': http_exception_options,
        }
