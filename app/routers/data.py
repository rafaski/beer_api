from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.sql import crud
from app.schemas import Beer, Hop
from app.dependencies.punk_client import punk_request
from app.routers.beers import get_db


router = APIRouter(tags=["data"])


@router.get("/data")
async def get_data(db: Session = Depends(get_db)):
    """
    [MANDATORY FIRST REQUEST] Making a request to Punk API, storing data in DB.
    It may take 15-20 seconds for the above operations to be completed.
    """
    for page in range(1, 6):
        beers = await punk_request(page=page)
        for beer in beers:
            temp = beer["method"]["fermentation"]["temp"]["value"]
            if temp:
                new_beer: Beer = Beer(
                    id=beer["id"],
                    name=beer["name"],
                    fermentation_temp=temp
                )
                crud.create_beer(db=db, beer=new_beer)

            hops = beer["ingredients"]["hops"]
            for hop in hops:
                if hops:
                    new_hop: Hop = Hop(
                        name=hop["name"],
                        amount=hop["amount"]["value"],
                        add=hop["add"],
                        attribute=hop["attribute"],
                        beer_id=beer["id"]
                    )
                    crud.create_hop(db=db, hop=new_hop)
    return {
        "message": ("Data successfully requested from Punk API and stored "
                    "in database. You can can query data now.")
    }
