from os import environ

import pytest
from fastapi import FastAPI
from asgi_lifespan import LifespanManager
from httpx import AsyncClient

from app.auth.services import JWTAuthService
from app.users.models import User
from app.users.schemes import UserCreateScheme


environ['APP_ENV'] = "test"


@pytest.fixture
def app() -> FastAPI:
    from app.main import init_app

    return init_app()


@pytest.fixture(autouse=True)
async def initialized_app(app: FastAPI) -> FastAPI:
    async with LifespanManager(app):
        yield app


@pytest.fixture
async def client(initialized_app: FastAPI):
    async with AsyncClient(app=initialized_app, base_url="http://localhost") as client:
        yield client


@pytest.fixture()
async def auth_user() -> User:
    return await User.create(UserCreateScheme(email='client@gmail.com', password='Client12345'))


@pytest.fixture
def authorized_client(client: AsyncClient, auth_user) -> AsyncClient:
    client.headers['Authorization'] = f"Bearer {JWTAuthService(User).gen_user_token(auth_user)}"
    return client
