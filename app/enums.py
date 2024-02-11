from enum import Enum


class ErrorTypes(str, Enum):
    """
    Enums for custom error types
    """

    # App errors
    UNKNOWN = "unknown"

    # API errors
    UNAUTHORIZED = "unauthorized"
    BAD_REQUEST = "bad_request"
    NOT_FOUND = "not_found"

    # Dependency errors
    PUNK_API_ERROR = "punk_api_error"
