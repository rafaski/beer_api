from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.sql import crud, models
from app.sql.database import SessionLocal, engine
from app.schemas import Beer, Hop
from app.dependencies.punk_client import punk_request

models.Base.metadata.create_all(bind=engine)

description = """
## Beer API ##
"""

app = FastAPI(
    title="Beer API",
    description="## Beer API ##"
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
async def startup_event(db: Session = Depends(get_db)):
    """
    Making a request to beer API, storing data in DB
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


@app.get("/avg_fermentation_temp_by_hop")
async def get_avg_fermentation_temp_by_hop_all(
        db: Session = Depends(get_db)):
    """
    Get average (mean) fermentation temperature for each type of hops
    """
    results = crud.get_avg_temp_by_hops(db=db)
    return results


@app.get("/avg_fermentation_temp_primary_hops")
async def get_avg_fermentation_temp_primary_hops(
        db: Session = Depends(get_db)):
    """
    Get average (mean) fermentation temperature for the primary hops
    """
    # TODO: Update CRUD operation with primary_hop logic
    results_by_hop = crud.get_avg_temp_by_hops(db=db)

    # Create a dict of avg hop fermentation temps to update results_primary_hops
    hop_avg_temp = {}
    for entry in results_by_hop:
        hop_avg_temp[entry["name"]] = entry["avg_beer_fermentation_temp"]

    # Get data for avg_fermentation_temp_primary_hops
    results_primary_hops = crud.get_avg_temp_primary_hops(db=db)
    for row in results_primary_hops:
        if row["hop_name"] in hop_avg_temp.keys():
            # Add key to row dict with avg_fermentation_temp_by_hop
            row["avg_beer_fermentation_temp"] = hop_avg_temp[row["hop_name"]]

    return results_primary_hops


@app.get("/get_10_most_used_hops")
async def get_10_most_used_hops(db: Session = Depends(get_db)):
    """
    Show the top 10 most used hops in the recipes
    """
    results = crud.get_ten_most_used_hops(db=db)
    return results


@app.get("/get_beers_by_hop/{hop_name}")
async def get_all_beers_by_hop(hop_name: str, db: Session = Depends(get_db)):
    """
    Show the beers that use a particular hop
    """
    results = crud.get_beers_by_hop(db=db, hop_name=hop_name)
    return results
