import json

import pytest
from httpx import AsyncClient
from starlette import status

from app.users.models import User
from app.users.schemes import UserCreateScheme

CREATE_USER_ROUTE = '/users/'
RETRIEVE_USER_ROUTE = '/users/me'

pytestmark = pytest.mark.asyncio


async def test_create_user(client: AsyncClient):
    request_payload = {"email": "some_email@gmail.com", "password": "some_password"}
    users_count_before = await User.all().count()

    response = await client.post(CREATE_USER_ROUTE, json=request_payload)
    assert response.status_code == status.HTTP_201_CREATED, response.json()
    assert len(await User.all()) == users_count_before + 1


async def test_fail_create_already_exist_user(client):
    user_1 = await User.create(UserCreateScheme(email='user1@gmail.com', password='some_password'))
    response = await client.post(CREATE_USER_ROUTE, json=dict(email=user_1.email, password='some_password'))
    assert response.status_code == status.HTTP_400_BAD_REQUEST


async def test_fail_create_user_with_wrong_email_format(client):
    response = await client.post(CREATE_USER_ROUTE, json=dict(email='some_data', password='some_password'))
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_retrieve_me(authorized_client, auth_user: User):
    response = await authorized_client.get(RETRIEVE_USER_ROUTE)
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data['id'] == auth_user.id
    assert 'first_name' in response_data
    assert 'last_name' in response_data
    assert 'username' in response_data
    assert 'email' in response_data
