from fastapi import Security
from fastapi.security import APIKeyHeader

from app.errors import Unauthorized
from app.settings import settings

#  Define the name of HTTP header to retrieve an API key from
api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)


async def verify_api_key(api_key: str = Security(api_key_header)) -> str:
    """
    Verify access api key via headers
    """
    if api_key == settings.api_key:
        return api_key
    raise Unauthorized()
