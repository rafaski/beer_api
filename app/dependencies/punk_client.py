import httpx

from app.errors import PunkApiException
from app.settings import settings


async def punk_request(page: int) -> dict:
    """
    HTTP requests to fetch all beer data from Punk API
    :return: a list of all beers
    """
    url = f"{settings.beer_api_base_url}?page={page}&per_page=80"

    # Attempt to make an async HTTP GET request to the API
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url=url)

            # Raise an HTTP error if the response status code is not 200 OK
            response.raise_for_status()

    except (httpx.HTTPError, httpx.RequestError):
        raise PunkApiException()

    # Parse the response JSON and return the beer data as a dictionary
    return response.json()
