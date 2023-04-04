from fastapi import FastAPI

from app.sql import models
from app.sql.database import SessionLocal, engine
from app.routers.beers import router as beer_router
from app.routers.data import router as data_router

description = """
## Beer API ##

### Supported operations are:
- `MANDATORY FIRST REQUEST` Making a request to Punk API, storing data in DB
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


@app.on_event("startup")
async def startup():
    """Connect to db at startup. Create tables"""
    models.Base.metadata.create_all(bind=engine)


@app.on_event("shutdown")
async def shutdown():
    SessionLocal.close_all()

app.include_router(data_router)
app.include_router(beer_router)
