from pydantic import BaseModel


class Hop(BaseModel):
    """
    Schema for hops SQL table
    """
    name: str
    amount: float
    add: str
    attribute: str
    beer_id: int

    class Config:
        orm_mode = True


class Beer(BaseModel):
    """
    Schema for beers SQL table
    """
    id: int
    name: str
    fermentation_temp: int

    class Config:
        orm_mode = True
