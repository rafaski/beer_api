from sqlalchemy.orm import Session
from sqlalchemy import func

from app.sql import models
from app.schemas import Hop, Beer


def create_beer(db: Session, beer: Beer) -> None:
    """Save a new beer to db"""
    new_beer = models.Beer(**beer.dict())
    db.add(new_beer)
    db.commit()


def create_hop(db: Session, hop: Hop) -> None:
    """Save a new hop to db"""
    new_hop = models.Hop(**hop.dict())
    db.add(new_hop)
    db.commit()


def get_avg_temp_by_hops(db: Session) -> list[models.Hop]:
    """
    Get an average fermentation temperature by hop
    """
    results = db.query(models.Hop.name, func.round(func.avg(
        models.Beer.fermentation_temp), 1).label(
        'avg_beer_fermentation_temp')).join(
        models.Beer, models.Hop.beer_id == models.Beer.id).group_by(
        models.Hop.name).all()
    return results


def get_avg_temp_primary_hops(db: Session):
    """
    Get average (mean) fermentation temperature for the primary hops
    """
    # Calculate the primary hop for each beer along with its maximum amount
    primary_query = db.query(
        models.Beer.id,
        models.Beer.name,
        models.Hop.name.label('primary_hop_name'),
        func.max(models.Hop.amount).label('max_amount')).join(
        models.Hop).group_by(
        models.Beer.id,
        models.Beer.name,
        models.Hop.name).having(
        models.Hop.amount == func.max(models.Hop.amount)).subquery()

    # Calculate the average fermentation temperature for each hop
    secondary_query = db.query(
        models.Hop.name.label('hop_name'),
        func.round(func.avg(models.Beer.fermentation_temp), 1).label(
        'avg_beer_fermentation_temp')).join(
        models.Beer, models.Hop.beer_id == models.Beer.id).group_by(
        models.Hop.name).subquery()

    # Join above queries for show results
    results = db.query(
        primary_query.c.id,
        primary_query.c.name,
        primary_query.c.primary_hop_name,
        primary_query.c.max_amount,
        secondary_query.c.avg_beer_fermentation_temp).join(
        secondary_query,
        primary_query.c.primary_hop_name == secondary_query.c.hop_name).all()
    return results


def get_ten_most_used_hops(db: Session) -> list[models.Hop]:
    """
    Show the top 10 most used hops in the recipes
    """
    results = db.query(models.Hop.name, func.round(func.sum(
        models.Hop.amount), 1).label('total_amount')).group_by(
        models.Hop.name).order_by(func.round(func.sum(
        models.Hop.amount), 1).desc()).limit(10)
    return results


def get_beers_by_temp(db: Session, temp: int) -> list[models.Beer]:
    """
    Get all beers that have a fermentation temperature greater than X
    """
    results = db.query(models.Beer).filter(
        models.Beer.fermentation_temp > temp).order_by(
        models.Beer.name).all()
    return results


def get_hops_by_amount(db: Session, amount: int) -> list[models.Hop]:
    """
    Get all hops that have an amount greater than or equal to X
    """
    results = db.query(models.Hop).filter(models.Hop.amount >= amount).order_by(
        models.Hop.amount.desc()).all()
    return results


def get_beers_by_hop(db: Session, hop_name: str) -> list[models.Beer]:
    """
    Get all beers that have a hop with the name X
    and order them by fermentation temperature
    """
    results = db.query(models.Beer).join(models.Hop).filter(
        models.Hop.name == hop_name).order_by(
        models.Beer.fermentation_temp).all()
    return results


def get_beers_with_highest_hop_amount(
    db: Session, hop_name: str
    ) -> list[models.Beer]:
    """
    Get the beers with the highest amount of a specific hop
    """
    # Select the beer IDs and the maximum hop amount
    subquery = db.query(models.Hop.beer_id, func.max(models.Hop.amount).label(
        'max_amount')).filter(models.Hop.name == hop_name).group_by(
        models.Hop.beer_id).subquery()

    # Filter the results to only include the rows where the hop amount is equal
    # to the maximum hop amount for that beer
    results = db.query(models.Beer).join(
        subquery,
        models.Beer.id == subquery.c.beer_id
        ).filter(models.Hop.amount == subquery.c.max_amount).all()

    return results
