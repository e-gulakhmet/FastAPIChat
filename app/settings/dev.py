from pydantic import Field

from app.settings import AppSettings


class DevAppSettings(AppSettings):
    debug: bool = True

    postgres_user: str = Field("main", env="POSTGRES_USER")
    postgres_password: str = Field("main", env="POSTGRES_PASSWORD")
    postgres_db: str = Field("main", env="POSTGRES_DB")
    postgres_port: str = Field("5432", env="POSTGRES_PORT")
    postgres_host: str = Field("localhost", env="POSTGRES_HOST")

    class Config(AppSettings.Config):
        env_file = ".env"