import json

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette import status

from app.core import db
from app.core.config import get_settings
from app.main import app

from app.users import crud
from app.users.models import User
from app.users.schemes import UserCreateSchema


CREATE_USER_ROUTE = '/users/'
RETRIEVE_USER_ROUTE = '/users/me'
LOGIN_ROUTE = '/users/login'


engine = create_async_engine(get_settings().test_database_url, echo=False, future=True)


async def get_test_session():
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session

app.dependency_overrides[db.get_session] = get_test_session


@pytest.fixture
async def auth_user() -> User:
    return await crud.create(UserCreateSchema(email='client@gmail.com', password='Client12345'))


@pytest.fixture
async def not_auth_client():
    async with AsyncClient(app=app, base_url="http://localhost") as client:
        yield client


@pytest.fixture
async def db_session():
    async for session in db.get_session():
        yield session


# @pytest.fixture
# async def db_session():
#     return Depends(db.get_session)


@pytest.mark.asyncio
async def test_create_user(not_auth_client: AsyncClient, db_session):
    request_payload = {"email": "some_email@gmail.com", "password": "some_password"}
    # users = await crud.get_multi(db_session)
    users = (await db_session.execute(select(User))).all()
    users_count_before = len(users)

    response = await not_auth_client.post(CREATE_USER_ROUTE, json=request_payload)
    assert response.status_code == status.HTTP_201_CREATED, response.json()
    users = (await db_session.execute(select(User))).all()
    assert len(users) == users_count_before + 1


# async def test_fail_create_already_exist_user(client, db_session: AsyncSession = Depends(db.get_session)):
#     user_1 = await crud.create(db_session, UserCreateSchema(email='user1@gmail.com', password='some_password'))
#     response = client.post(CREATE_USER_ROUTE, data=json.dumps(dict(email=user_1.email, password=user_1.password)))
#     assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_fail_create_user_with_wrong_email_format(client):
    response = client.post(CREATE_USER_ROUTE, data=json.dumps(dict(email='some_data', password='some_password')))
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_retrieve_me(client):
    response = client.get(RETRIEVE_USER_ROUTE)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    response_data = response.json()
    assert response_data['id'] == client.id
    assert 'first_name' in response_data
    assert 'last_name' in response_data
    assert 'username' in response_data
    assert 'email' in response_data


def test_login(client):
    response = client.post(LOGIN_ROUTE, data=json.dumps(dict(email=client.email, password=client.password)))
    assert response.status_code == status.HTTP_200_OK
    assert 'access_token' in response.json()


def test_fail_login_with_wrong_email(client):
    response = client.post(LOGIN_ROUTE, data=json.dumps(dict(email='sfdsd@gmail.com', password='tarter')))
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_fail_login_with_wrong_password(client):
    response = client.post(LOGIN_ROUTE, data=json.dumps(dict(email=client.email, password='tarter')))
    assert response.status_code == status.HTTP_400_BAD_REQUEST
