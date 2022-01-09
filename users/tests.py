import json

import pytest
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette import status

from core import db
from users.crud import crud
from users.schemes import UserCreateSchema


CREATE_USER_ROUTE = '/users/'
RETRIEVE_USER_ROUTE = '/users/me'
LOGIN_ROUTE = '/users/login'


def test_create_user(client):
    request_payload = {"email": "some_email@gmail.com", "password": "some_password"}

    response = client.post(CREATE_USER_ROUTE, data=json.dumps(request_payload))

    assert response.status_code == status.HTTP_201_CREATED
    response_data = response.json()
    assert response_data['id'] == client.id


def test_fail_create_already_exist_user(client, db_session: AsyncSession = Depends(db.get_session)):
    user_1 = await crud.create(db_session, UserCreateSchema(email='user1@gmail.com', password='some_password'))
    response = client.post(CREATE_USER_ROUTE, data=json.dumps(dict(email=user_1.email, password=user_1.password)))
    assert response.status_code == status.HTTP_400_BAD_REQUEST


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
