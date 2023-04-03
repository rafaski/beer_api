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
POSTGRES_PASSWORD = load_variable(name="POSTGRES_PASSWORD", default="postgres")
DATABASE_URL = load_variable(
    name="DATABASE_URL",
    default=(f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@postgresserver/db")
)
