import httpx
import asyncio
from pprint import pprint


async def punk_request() -> list[dict]:
    """
    HTTP requests to fetch all beer data from Punk API
    :return: a list of all beers
    """
    all_beers = []

    # overwriting default 5 sec timeout
    timeout = httpx.Timeout(timeout=15.0, read=None)

    # fetching all beer data
    for page in range(1, 6):
        url = f"https://api.punkapi.com/v2/beers?page={page}&per_page=80"
        async with httpx.AsyncClient() as client:
            response = await client.get(url=url, timeout=timeout)
            # all_beers.extend(response.json())
            for beer in response.json():
                if not beer.get("id") == 169:
                    new_beer = {
                        "id": beer.get("id"),
                        "name": beer.get("name"),
                        "fermentation": beer.get("method").get(
                            "fermentation"
                        ).get("temp"),
                        "hops": beer.get("ingredients").get("hops")
                    }
                    # print(new_beer)
                    all_beers.append(new_beer)

    # TODO: REMOVE LIST, extract directly to DB from JSON response
    return all_beers

loop = asyncio.get_event_loop()
pprint(loop.run_until_complete(punk_request()))
