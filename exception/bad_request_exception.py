from http import HTTPStatus
from .http_exception import HttpException
from typing import Union , Dict , Any , Optional

class BadRequestException(HttpException):
    def __init__(self, response: Union[str, Dict[str, Any]] = HTTPStatus.BAD_REQUEST.phrase, options: Optional[Dict[str, Any]] = None):
        super().__init__(response, HTTPStatus.BAD_REQUEST, options)
