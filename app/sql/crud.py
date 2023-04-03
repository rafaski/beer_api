from sqlalchemy.orm import Session
from sqlalchemy import func

from app.sql import models
from app.schemas import Hop, Beer


def create_beer(db: Session, beer: Beer) -> None:
    """Save a new beer to db"""
    new_beer = models.Beer(**beer.dict())
    db.add(new_beer)
    db.commit()


def get_all_beers(db: Session) -> list[models.Beer] | None:
    """Get all beers from db"""
    all_beers = db.query(models.Beer).all()
    return all_beers


def get_beer_by_id(db: Session, beer_id: int) -> models.Beer | None:
    """Get beer by name"""
    beer = db.query(models.Beer).filter(
        models.Beer.id == beer_id
    ).first()
    return beer


def create_hop(db: Session, hop: Hop) -> None:
    """Save a new hop to db"""
    new_hop = models.Hop(**hop.dict())
    db.add(new_hop)
    db.commit()


def get_by_hop_name(db: Session, hop_name: str) -> list[models.Hop] | None:
    """Get a list of hops by name"""
    matching_hops = db.query(models.Hop).filter(
        models.Hop.name == hop_name
    ).all()
    return matching_hops


def get_avg_temp_by_hops(db: Session) -> list[models.Hop]:
    """
    Get an average fermentation temperature by hop
    SQL statement:
    SELECT hops.name, ROUND(AVG(beers.fermentation_temp), 1)
    AS avg_beer_fermentation_temp FROM hops
    INNER JOIN beers ON hops.beer_id=beers.id GROUP BY hops.name

    """
    results = db.query(models.Hop.name, func.round(func.avg(
        models.Beer.fermentation_temp), 1).label(
        'avg_beer_fermentation_temp')).join(
        models.Beer, models.Hop.beer_id == models.Beer.id).group_by(
        models.Hop.name).all()
    return results


def get_avg_temp_primary_hops(db: Session) -> list[models.Hop]:
    """
    Get average (mean) fermentation temperature for the primary hops
    TODO: SQL statement:
    TBA
    """