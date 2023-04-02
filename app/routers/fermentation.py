from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.sql import crud, models
from app.sql.database import SessionLocal, engine
from app.schemas import Beer, Hop


models.Base.metadata.create_all(bind=engine)

router = APIRouter(tags=["fermentation"])


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/avg_fermentation_temp_by_hop/all")
async def get_avg_fermentation_temp_by_hop_all(
        db: Session = Depends(get_db)) -> list[Hop]:
    """
    Get an average fermentation temperature for all available hops
    """
    # results = crud.get_beer_by_id(db=db, beer_id=1)
    results = crud.get_all_beers(db=db)
    return results
