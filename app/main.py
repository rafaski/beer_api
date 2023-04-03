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
async def startup_event() -> None:
    """
    Making a request to beer API, storing data in DB
    """
    await punk_request(db=get_db)


@app.get("/avg_fermentation_temp_by_hop")
async def get_avg_fermentation_temp_by_hop_all(
        db: Session = Depends(get_db)) -> list[Hop]:
    """
    Get average (mean) fermentation temperature for each type of hops
    """
    results = crud.get_all_beers(db=db)
    return results


@app.get("/avg_fermentation_temp_primary_hops")
async def get_avg_fermentation_temp_primary_hops(
        db: Session = Depends(get_db)) -> list[Hop]:
    """
    Get average (mean) fermentation temperature for the primaryhops
    """
    results = crud.get_all_beers(db=db)
    return results
