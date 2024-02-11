from fastapi import FastAPI

from app.routers.beers import router as beer_router
from app.routers.data import router as data_router
from app.routers.health import router as health_router
from app.settings import settings
from app.sql import models
from app.sql.database import SessionLocal, engine

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
"""

app = FastAPI(
    title="Beer API",
    description=description,
    docs_url=None if settings.is_production else "/docs",
)


@app.on_event("startup")
async def startup():
    """Connect to db at startup. Create tables"""
    models.Base.metadata.create_all(bind=engine)


@app.on_event("shutdown")
async def shutdown():
    """Close all open database connections"""
    SessionLocal.close_all()


app.include_router(data_router)
app.include_router(beer_router)
app.include_router(health_router)
