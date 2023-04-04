from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.sql import crud, models
from app.sql.database import SessionLocal, engine
from app.schemas import Beer, Hop
from app.dependencies.punk_client import punk_request
from app.errors import NotFound

models.Base.metadata.create_all(bind=engine)

description = """
## Beer API ##

### Supported operations are:
- `MANDATORY` Making a request to Punk API, storing data in DB
- Get average fermentation temperature for each type of hops
- Get average fermentation temperature for the primary hops
- Show the top 10 most used hops in the recipes
- Get all beers that have a fermentation temperature greater than X
- Get all hops that have an amount greater than or equal to X
- Get all beers that have a hop with the name X
- Get the beers with the highest amount of a specific hop
"""

app = FastAPI(
    title="Beer API",
    description=description
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/data")
async def get_data(db: Session = Depends(get_db)):
    """
    [MANDATORY] Making a request to Punk API, storing data in DB
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
    return {"message": "Data requested from Punk API and stored in database"}


@app.get("/avg_fermentation_temp_by_hop")
async def get_avg_fermentation_temp_by_hop_all(
        db: Session = Depends(get_db)):
    """
    Get average fermentation temperature for each type of hops
    """
    results = crud.get_avg_temp_by_hops(db=db)
    return results


@app.get("/avg_fermentation_temp_primary_hops")
async def get_avg_fermentation_temp_primary_hops(
    db: Session = Depends(get_db)):
    """
    Get average fermentation temperature for the primary hops
    """
    results_primary_hops = crud.get_avg_temp_primary_hops(db=db)
    return results_primary_hops


@app.get("/most_used_hops")
async def get_10_most_used_hops(db: Session = Depends(get_db)):
    """
    Show the top 10 most used hops in the recipes
    """
    results = crud.get_ten_most_used_hops(db=db)
    return results


@app.get("/beers_by_temp")
async def get_beers_by_temp(temp: int, db: Session = Depends(get_db)):
    """
    Get all beers that have a fermentation temperature greater than X
    """
    results = crud.get_beers_by_temp(db=db, temp=temp)
    if not results:
        raise NotFound(details="Results not found.")
    return results


@app.get("/hops_by_amount")
async def get_hops_by_amount(amount: int, db: Session = Depends(get_db)):
    """
    Get all hops that have an amount greater than or equal to X
    """
    results = crud.get_hops_by_amount(db=db, amount=amount)
    if not results:
        raise NotFound(details="Results not found.")
    return results


@app.get("/beers_by_hop")
async def get_beers_by_hop(hop_name: str, db: Session = Depends(get_db)):
    """
    Get all beers that have a hop with the name X
    and order them by fermentation temperature
    """
    results = crud.get_beers_by_hop(db=db, hop_name=hop_name)
    if not results:
        raise NotFound(details="Results not found.")
    return results


@app.get("/beers_with_highest_hop_amount")
async def get_beers_with_highest_hop_amount(
    hop_name: str,
    db: Session = Depends(get_db)
    ):
    """
    Get the beers with the highest amount of a specific hop
    """
    results = crud.get_beers_with_highest_hop_amount(db=db, hop_name=hop_name)
    if not results:
        raise NotFound(details="Results not found.")
    return results
