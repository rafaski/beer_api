from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.settings import POSTGRES_USER, POSTGRES_PASSWORD

DATABASE_URL = "sqlite:///./sql_app.db"

# Postgres
# DATABASE_URL = (f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
#                 f"@postgresserver/db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# TODO: Replace to PostgreSQL
