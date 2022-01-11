from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from tortoise.contrib.starlette import register_tortoise

from app.settings import tortoise_settings
from app.settings import app_settings
from app.auth.routers import router as auth_router
from app.core.routers import router as core_router
from app.users.routers import router as users_router


def init(app: FastAPI):
    """ Init routers and etc. """
    init_routers(app)
    init_db(app)
    init_middlewares(app)


def init_db(app: FastAPI):
    """ Init database models. """
    register_tortoise(
        app,
        db_url=tortoise_settings.db_url,
        generate_schemas=tortoise_settings.generate_schemas,
        modules=tortoise_settings.modules,
    )


def init_routers(app: FastAPI):
    """ Initialize routers """
    app.include_router(auth_router, prefix='/auth', tags=['auth'])
    app.include_router(core_router, prefix='/core', tags=['core'])
    app.include_router(users_router, prefix='/users', tags=['users'])


def init_middlewares(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=app_settings.cors_allow_origins,
        allow_credentials=['*'],
        allow_methods=['*'],
        allow_headers=app_settings.cors_allow_headers,
    )
