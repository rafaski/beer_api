from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.sql import crud
from app.sql.database import SessionLocal
from app.auth.verify import verify_api_key


router = APIRouter(dependencies=[Depends(verify_api_key)])


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/avg_fermentation_temp_by_hop", tags=["hops"])
async def get_avg_fermentation_temp_by_hop_all(
    db: Session = Depends(get_db)
):
    """
    Get average fermentation temperature for each type of hops
    """
    results = crud.get_avg_temp_by_hops(db=db)
    return results


@router.get("/avg_fermentation_temp_primary_hops", tags=["hops"])
async def get_avg_fermentation_temp_primary_hops(
    db: Session = Depends(get_db)
):
    """
    Get average fermentation temperature for the primary hops
    """
    results_primary_hops = crud.get_avg_temp_primary_hops(db=db)
    return results_primary_hops


@router.get("/most_used_hops", tags=["hops"])
async def get_10_most_used_hops(db: Session = Depends(get_db)):
    """
    Show the top 10 most used hops in the recipes
    """
    results = crud.get_ten_most_used_hops(db=db)
    return results


@router.get("/beers_by_temp", tags=["beers"])
async def get_beers_by_temp(temp: int, db: Session = Depends(get_db)):
    """
    Get all beers that have a fermentation temperature greater than X
    """
    results = crud.get_beers_by_temp(db=db, temp=temp)
    return results


@router.get("/hops_by_amount", tags=["hops"])
async def get_hops_by_amount(amount: int, db: Session = Depends(get_db)):
    """
    Get all hops that have an amount greater than or equal to X
    """
    results = crud.get_hops_by_amount(db=db, amount=amount)
    return results


@router.get("/beers_by_hop", tags=["beers"])
async def get_beers_by_hop(hop_name: str, db: Session = Depends(get_db)):
    """
    Get all beers that have a hop with the name X
    and order them by fermentation temperature
    """
    hop_name = hop_name.capitalize()
    results = crud.get_beers_by_hop(db=db, hop_name=hop_name)
    return results
