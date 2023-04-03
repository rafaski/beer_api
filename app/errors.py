from fastapi import status

from app.enums import ErrorTypes


class AppException(Exception):
    """
    Base app exception class
    """
    http_status_code: status = status.HTTP_500_INTERNAL_SERVER_ERROR
    error_type: ErrorTypes = ErrorTypes.UNKNOWN
    details: str = None

    def __init__(
        self,
        http_status_code: status = None,
        error_type: str = None,
        details: str = None
    ):
        self.http_status_code = http_status_code or self.http_status_code
        self.error_type = error_type or self.error_type
        self.details = details or self.details
        super(AppException, self).__init__()


class ApiException(AppException):
    pass


class BadRequest(ApiException):
    http_status_code: status = status.HTTP_400_BAD_REQUEST
    error_type: ErrorTypes = ErrorTypes.BAD_REQUEST
    details: str = "Bad request"


class NotFound(ApiException):
    http_status_code: status = status.HTTP_404_NOT_FOUND
    error_type: ErrorTypes = ErrorTypes.NOT_FOUND
    details: str = "Bad request"
