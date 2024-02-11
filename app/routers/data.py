from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app.auth.verify import verify_api_key
from app.dependencies.punk_client import punk_request
from app.routers.beers import get_db
from app.schemas import Beer, Hop
from app.sql import crud

router = APIRouter(tags=["data"], dependencies=[Depends(verify_api_key)])


@router.get("/data")
async def get_data(db: Session = Depends(get_db)):
    """
    [MANDATORY FIRST REQUEST] Making a request to Punk API, storing data in DB.
    It may take 20-30 seconds for these operations to be completed.
    """
    # Loop through each page of Punk API data to fetch beer information
    for page in range(1, 6):
        # Make HTTP request to the Punk API to fetch beer data
        beers = await punk_request(page=page)

        # Loop through each beer in the API response and extract  data
        for beer in beers:
            try:
                # Extract the fermentation temperature from the API response
                temp = beer["method"]["fermentation"]["temp"]["value"]

                # Drop beers with None temp or temp > 32
                if temp and temp < 32:
                    # Create new Beer object using the extracted data
                    new_beer: Beer = Beer(
                        id=beer["id"], name=beer["name"], fermentation_temp=temp
                    )

                    # Save the Beer object to the database
                    crud.create_beer(db=db, beer=new_beer)

                    # Extract hop data from the API response
                    hops = beer["ingredients"]["hops"]
                    for hop in hops:
                        # Check if the hop data is not None
                        if hop:
                            # Create new Hop object using the extracted data
                            new_hop: Hop = Hop(
                                name=hop["name"],
                                amount=hop["amount"]["value"],
                                add=hop["add"],
                                attribute=hop["attribute"],
                                beer_id=beer["id"],
                            )

                            # Save the Hop object to the database
                            crud.create_hop(db=db, hop=new_hop)

            except KeyError:
                # Handle the exception when the JSON response layout changes
                raise HTTPException(
                    status_code=500,
                    detail=(
                        "JSON response structure has changed. Please update "
                        "the code."
                    )
                )

            except Exception:
                # Handle the exception for data processing or db operations
                raise HTTPException(
                    status_code=500,
                    detail=(
                        "An error occurred while processing data or storing it "
                        "in the database."
                    )
                )

    return JSONResponse(content={
        "message": (
            "Data successfully requested from Punk API and stored in database. "
            "You can query data now."
        )
    })