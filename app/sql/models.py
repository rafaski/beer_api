from sqlalchemy.orm import relationship
from sqlalchemy import (Column, Integer, String, Float, ForeignKey)

from app.sql.database import Base


class Beer(Base):
    __tablename__ = "beers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    fermentation_temp = Column(Float)

    hops = relationship("Hop", back_populates="beer")


class Hop(Base):
    __tablename__ = "hops"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True)
    amount = Column(Float)
    add = Column(String, index=True)
    attribute = Column(String, index=True)
    beer_id = Column(Integer, ForeignKey("beers.id"))

    beer = relationship("Beer", back_populates="hops")
