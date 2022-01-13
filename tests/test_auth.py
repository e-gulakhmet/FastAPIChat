import json

import pytest
from starlette import status

from app.users.models import User

pytestmark = pytest.mark.asyncio


LOGIN_ROUTE = '/auth/access-token'


async def test_login(client, test_data_service, auth_user: User):
    response = await client.post(LOGIN_ROUTE, json=dict(email=auth_user.email,
                                                        password=test_data_service.USER_PASSWORD))
    assert response.status_code == status.HTTP_200_OK, response.json()
    assert 'access_token' in response.json()


async def test_fail_login_with_wrong_email(client, test_data_service):
    response = await client.post(LOGIN_ROUTE, json=dict(email='sfdsd@gmail.com',
                                                        password=test_data_service.USER_PASSWORD))
    assert response.status_code == status.HTTP_400_BAD_REQUEST


async def test_fail_login_with_wrong_password(client, test_data_service):
    user = await test_data_service.create_user()
    response = await client.post(LOGIN_ROUTE, json=dict(email=user.email, password='tarter'))
    assert response.status_code == status.HTTP_400_BAD_REQUEST
