import time
from datetime import timedelta, datetime
from typing import Optional

import jwt
from passlib.context import CryptContext

from app.auth.schemes import CredentialsSchema
from app.settings import app_settings


class AuthService:
    def __init__(self, user_model):
        self.user_model = user_model

    async def auth(self, credentials: CredentialsSchema):
        """
        :return: user by specified credentials
        """
        if credentials.email:
            user = await self.user_model.get_by_email(credentials.email)
        elif credentials.username:
            user = await self.user_model.get_by_username(credentials.username)
        else:
            raise ValueError('email or username must be specified')

        if user is None:
            return None

        if not self._verify_password(credentials.password, user.hashed_password):
            return None

        return user

    @staticmethod
    def _verify_password(plain_password, hashed_password) -> bool:
        return CryptContext(schemes=["bcrypt"], deprecated="auto").verify(plain_password, hashed_password)


class JWTAuthService:
    def __init__(self, user_model):
        self.user_model = user_model

    def gen_user_token(self, user) -> str:
        user_id = user.id
        payload = {'user_id': user_id}
        return self.gen_access_token(payload, timedelta(minutes=app_settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES))

    @staticmethod
    def gen_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, app_settings.JWT_SECRET, algorithm=app_settings.JWT_ALGORITHM)

        return encoded_jwt

    @staticmethod
    def decode_token(token: str) -> dict:
        decoded_token = jwt.decode(token, app_settings.JWT_SECRET, algorithms=[app_settings.JWT_ALGORITHM])
        return decoded_token if decoded_token["exp"] >= time.time() else None

    async def get_user_from_token_payload(self, payload: dict):
        user_id = payload['user_id']
        return await self.user_model.get_by_id(user_id)

    async def get_user_from_token(self, token: str):
        payload = self.decode_token(token)
        user = await self.get_user_from_token_payload(payload)
        return user
