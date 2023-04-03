import httpx
from fastapi import status, HTTPException


async def punk_request(page: int) -> dict:
    """
    HTTP requests to fetch all beer data from Punk API
    :return: a list of all beers
    """
    url = f"https://api.punkapi.com/v2/beers?page={page}&per_page=80"
    async with httpx.AsyncClient() as client:
        response = await client.get(url=url)

    if not response.status_code == 200:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Failed to fetch data from the PunkAPI'
        )
    beers = response.json()
    return beers
