from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "FastAPIChat"
    allow_origins: list[str] = ['*']
    allow_headers: list[str] = ['*']
    # Database
    database_url: str = 'postgresql+asyncpg://main:main@localhost:5432/main'
    test_database_url: str = 'postgresql+asyncpg://test:test@localhost:5435/test'
    # JWT
    jwt_secret: str = 'fake_secret'
    jwt_access_token_expire_minutes: int = 30
    jwt_algorithm = 'HS256'


@lru_cache()
def get_settings():
    return Settings()


