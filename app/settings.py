from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Settings class to manage environment variables.
    """

    api_key: str
    is_production: bool = False

    # postgres
    postgres_user: str
    postgres_password: str
    postgres_server: str
    postgres_port: str
    postgres_db: str

    @property
    def postgres_db_url(self) -> str:
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}@"
            f"{self.postgres_server}:{self.postgres_port}/{self.postgres_db}"
        )

    sqlite_db_url: str = "sqlite:///./sql_app.db"

    # beer api
    beer_api_base_url: str = "https://api.punkapi.com/v2/beers"

    class Config:
        env_prefix = ""


settings = Settings()
