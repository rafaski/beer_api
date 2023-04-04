import httpx

from app.errors import BadRequest


async def punk_request(page: int) -> dict:
    """
    HTTP requests to fetch all beer data from Punk API
    :return: a list of all beers
    """
    url = f"https://api.punkapi.com/v2/beers?page={page}&per_page=80"
    async with httpx.AsyncClient() as client:
        response = await client.get(url=url)

    if not response.status_code == 200:
        raise BadRequest(details='Failed to fetch data from the PunkAPI')

    beers = response.json()
    return beers
