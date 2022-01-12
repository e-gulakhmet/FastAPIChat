from typing import Any, Dict

from pydantic.tools import lru_cache

from app.settings.base import BaseAppSettings


class AppSettings(BaseAppSettings):
    debug: bool = False
    docs_url: str = "/docs"
    openapi_prefix: str = ""
    openapi_url: str = "/openapi.json"
    redoc_url: str = "/redoc"
    title: str = "FastAPIChat"

    cors_allow_origins: list[str] = ['*']
    cors_allow_headers: list[str] = ['*']

    database_url: str
    max_connection_count: int = 10
    min_connection_count: int = 10

    jwt_secret: str
    jwt_access_token_expire_minutes: int
    jwt_algorithm: str = 'HS256'

    postgres_user: str = 'main'
    postgres_password: str = 'main'
    postgres_db: str = 'main'
    postgres_port: str = '5432'
    postgres_host: str = '0.0.0.0'
    database_url = f"postgresql+asyncpg://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"

    class Config:
        validate_assignment = True

    @property
    def fastapi_kwargs(self) -> Dict[str, Any]:
        return {
            "debug": self.debug,
            "docs_url": self.docs_url,
            "openapi_prefix": self.openapi_prefix,
            "openapi_url": self.openapi_url,
            "redoc_url": self.redoc_url,
            "title": self.title,
        }