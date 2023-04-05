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


def get_avg_temp_by_hops(db: Session) -> list[dict]:
    """
    Get an average fermentation temperature by hop

    Logic:
    Joins the beers and hops tables, groups by the hop name,
    and calculates the average fermentation temperature.
    """
    results = db.query(models.Hop.name, func.round(func.avg(
        models.Beer.fermentation_temp), 1).label(
        'avg_beer_fermentation_temp')).join(
        models.Beer, models.Hop.beer_id == models.Beer.id).group_by(
        models.Hop.name).all()
    # Returning results directly failed with docker, this workaround works
    return [r._asdict() for r in results]


def get_avg_temp_primary_hops(db: Session) -> list[dict]:
    """
    Get average (mean) fermentation temperature for the primary hops

    Logic:
    primary_query: get primary hop for each beer along with its maximum amount.
    Some beers had the same hops within a single recipe,
    I made sure to calculate the sum first,
    then showcase only those with the highest value per beer.
    Some beers have several hops with the same amount as showcased
    in the example data in README.md.
    secondary_query: calculates average fermentation temperature for each hop.
    results: joined the above subqueries to showcase results.
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
    # Returning results directly failed with docker, this workaround works
    return [r._asdict() for r in results]


def get_ten_most_used_hops(db: Session) -> dict:
    """
    Show the top 10 most used hops in the recipes

    Logic:
    Get hop.name, sum the hop.amount column and round it.
    Group results by hop.name. Sort results in descending order
    based on the rounded sum of the amount column and limit results to top 10.
    """
    results = db.query(models.Hop.name, func.round(func.sum(
        models.Hop.amount), 1).label('total_amount')).group_by(
        models.Hop.name).order_by(func.round(func.sum(
        models.Hop.amount), 1).desc()).limit(10)
    return results


def get_beers_by_temp(db: Session, temp: int) -> list[dict]:
    """
    Get all beers that have a fermentation temperature greater than X

    Logic:
    Query beers table. Filter results by privided temp: beer.temp > temp.
    Sort results by name.
    """
    results = db.query(models.Beer).filter(
        models.Beer.fermentation_temp > temp).order_by(
        models.Beer.name).all()
    return results


def get_hops_by_amount(db: Session, amount: int) -> list[dict]:
    """
    Get all hops that have an amount greater than or equal to X

    Logic:
    Query hops table. Filter results by provided amount: hop.amount >= amount.
    Sort in descending order by the amount column.
    """
    results = db.query(models.Hop).filter(
        models.Hop.amount >= amount).order_by(
        models.Hop.amount.desc()).all()
    return results


def get_beers_by_hop(db: Session, hop_name: str) -> list[dict]:
    """
    Get all beers that have a hop with the name X
    and order them by fermentation temperature

    Logic:
    Join beers and hops tables. Filter hop.name by provided hop_name.
    Order results by beer.fermentation_temp
    """
    results = db.query(models.Beer).join(models.Hop).filter(
        models.Hop.name == hop_name).order_by(
        models.Beer.fermentation_temp).all()
    return results
