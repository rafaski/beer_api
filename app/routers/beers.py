from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.sql import crud
from app.sql.database import SessionLocal
from app.errors import NotFound


router = APIRouter(tags=["beers"])


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/avg_fermentation_temp_by_hop")
async def get_avg_fermentation_temp_by_hop_all(
        db: Session = Depends(get_db)):
    """
    Get average fermentation temperature for each type of hops
    """
    results = crud.get_avg_temp_by_hops(db=db)
    return results


@router.get("/avg_fermentation_temp_primary_hops")
async def get_avg_fermentation_temp_primary_hops(
    db: Session = Depends(get_db)):
    """
    Get average fermentation temperature for the primary hops
    """
    results_primary_hops = crud.get_avg_temp_primary_hops(db=db)
    return results_primary_hops


@router.get("/most_used_hops")
async def get_10_most_used_hops(db: Session = Depends(get_db)):
    """
    Show the top 10 most used hops in the recipes
    """
    results = crud.get_ten_most_used_hops(db=db)
    return results


@router.get("/beers_by_temp")
async def get_beers_by_temp(temp: int, db: Session = Depends(get_db)):
    """
    Get all beers that have a fermentation temperature greater than X
    """
    results = crud.get_beers_by_temp(db=db, temp=temp)
    return results


@router.get("/hops_by_amount")
async def get_hops_by_amount(amount: int, db: Session = Depends(get_db)):
    """
    Get all hops that have an amount greater than or equal to X
    """
    results = crud.get_hops_by_amount(db=db, amount=amount)
    return results


@router.get("/beers_by_hop")
async def get_beers_by_hop(hop_name: str, db: Session = Depends(get_db)):
    """
    Get all beers that have a hop with the name X
    and order them by fermentation temperature
    """
    results = crud.get_beers_by_hop(db=db, hop_name=hop_name)
    return results


@router.get("/beers_with_highest_hop_amount")
async def get_beers_with_highest_hop_amount(
    hop_name: str,
    db: Session = Depends(get_db)
    ):
    """
    Get the beers with the highest amount of a specific hop
    """
    results = crud.get_beers_with_highest_hop_amount(db=db, hop_name=hop_name)
    return results
