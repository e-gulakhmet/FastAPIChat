from pydantic import BaseSettings


APPS = [
    'users',
]


class AppSettings(BaseSettings):
    app_name: str = "FastAPIChat"
    cors_allow_origins: list[str] = ['*']
    cors_allow_headers: list[str] = ['*']
    # Database
    database_url: str = 'postgresql+asyncpg://main:main@localhost:5432/main'
    test_database_url: str = 'postgresql+asyncpg://test:test@localhost:5435/test'
    # JWT
    jwt_secret: str = 'fake_secret'
    jwt_access_token_expire_minutes: int = 30
    jwt_algorithm = 'HS256'

    apps = [APPS]


