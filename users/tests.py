import json

import pytest
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette import status

from core import db
from users.crud import crud
from users.schemes import UserCreateSchema


USER_CREATE_ROUTE = '/users/'


def test_create_user(client):
    request_payload = {"email": "some_email@gmail.com", "password": "some_password"}
    response_payload = {
        "id": 1,
        "email": request_payload['email'],
        'first_name': None,
        'last_name': None,
        'username': None
    }

    response = client.post(USER_CREATE_ROUTE, data=json.dumps(request_payload))

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == response_payload


def test_fail_create_already_exist_user(client, db_session: AsyncSession = Depends(db.get_session)):
    user_1 = await crud.create(db_session, UserCreateSchema(email='user1@gmail.com', password='some_password'))
    response = client.post(USER_CREATE_ROUTE, data=json.dumps(dict(email=user_1.email, password=user_1.password)))
    assert response.status_code == status.HTTP_400_BAD_REQUEST
