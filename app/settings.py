import os
from typing import Any
from dotenv import load_dotenv

load_dotenv()


def load_variable(name: str, default: Any = None) -> str:
    variable = os.getenv(name, default)
    if variable is None:
        print(f"Unable to load variable {name}")
    return variable


# Postgres
POSTGRES_USER = load_variable(name="POSTGRES_USER", default="postgres")
POSTGRES_PASSWORD = load_variable(name="POSTGRES_PASSWORD", default="password")
POSTGRES_SERVER = load_variable(name="POSTGRES_SERVER", default="localhost")
POSTGRES_PORT = load_variable(name="POSTGRES_PORT", default=5432)
POSTGRES_DB = load_variable(name="POSTGRES_DB", default="db")
DATABASE_URL = (f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
                f"{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}")
