from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.settings import DATABASE_URL

# SQLite version
# DATABASE_URL = "sqlite:///./sql_app.db"
# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Postgres version
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
