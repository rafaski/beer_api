import os
from typing import Any
from dotenv import load_dotenv

load_dotenv()


def load_variable(name: str, default: Any = None) -> str:
    """
    Get environment variable from ENV file
    """
    variable = os.getenv(name, default)
    if variable is None:
        print(f"Unable to load variable {name}")
    return variable


# Postgres
POSTGRES_USER = load_variable(name="POSTGRES_USER")
POSTGRES_PASSWORD = load_variable(name="POSTGRES_PASSWORD")
POSTGRES_SERVER = load_variable(name="POSTGRES_SERVER")
POSTGRES_PORT = load_variable(name="POSTGRES_PORT")
POSTGRES_DB = load_variable(name="POSTGRES_DB")
DATABASE_URL = (f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
                f"{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}")
