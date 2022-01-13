from fastapi import FastAPI

from app.initializer import init
from app.settings.config import get_settings


def init_app() -> FastAPI:
    settings = get_settings()
    application = FastAPI(**settings.fastapi_kwargs)

    init(application)

    return application


app = init_app()
