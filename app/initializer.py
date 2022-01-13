from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from tortoise.contrib.starlette import register_tortoise

from app.auth.routers import router as auth_router
from app.core.routers import router as core_router
from app.settings.config import get_settings
from app.users.routers import router as users_router


def init(app: FastAPI):
    """ Init routers and etc. """
    init_routers(app)
    init_db(app)
    init_middlewares(app)


def init_db(app: FastAPI):
    """ Init database models. """
    settings = get_settings()
    register_tortoise(
        app,
        db_url=settings.database_url,
        generate_schemas=True,
        modules={'models': settings.models}
    )


def get_tortoise_config():
    settings = get_settings()
    return {
        'connections': {'default': settings.database_url},
        'apps': {
            'models': {
                'models': settings.models,
                'default_connection': 'default',
            }
        }
    }


TORTOISE_ORM = get_tortoise_config()


def init_routers(app: FastAPI):
    """ Initialize routers """
    app.include_router(auth_router)
    app.include_router(core_router)
    app.include_router(users_router)


def init_middlewares(app: FastAPI):
    settings = get_settings()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allow_origins,
        allow_credentials=['*'],
        allow_methods=['*'],
        allow_headers=settings.cors_allow_headers,
    )
