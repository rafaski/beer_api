from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.settings import settings

# SQLite
engine = create_engine(
    settings.sqlite_db_url,
    connect_args={"check_same_thread": False},
    pool_pre_ping=True
)

# Postgres
# engine = create_engine(settings.postgres_db_url, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
