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
async def startup_event(db: Session = Depends(get_db)) -> None:
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
        db: Session = Depends(get_db)) -> list[Hop]:
    """
    Get average (mean) fermentation temperature for each type of hops
    """
    results = crud.get_avg_temp_by_hops(db=db)
    return results


@app.get("/avg_fermentation_temp_primary_hops")
async def get_avg_fermentation_temp_primary_hops(
        db: Session = Depends(get_db)) -> list[Hop]:
    """
    Get average (mean) fermentation temperature for the primaryhops
    """
    # TODO: Update CRUD operation with primary_hop logic
    results = crud.get_avg_temp_primary_hops(db=db)
    return results
