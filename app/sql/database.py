from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.settings import DATABASE_URL

# Switch to SQLite if unable connecting to Postgres
# DATABASE_URL = "sqlite:///./sql_app.db"
# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Postgres
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
