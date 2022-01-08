import time
from datetime import timedelta, datetime
from typing import Optional

import jwt
from sqlmodel.ext.asyncio.session import AsyncSession

from core import settings
from users.models import User
from users.crud import crud


class JWTAuthService:
    def gen_user_token(self, user: User) -> str:
        user_id = user.id
        payload = {'user_id': user_id}
        return self.gen_access_token(payload, timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES))

    @staticmethod
    def gen_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

        return encoded_jwt

    @staticmethod
    def decode_token(token: str) -> dict:
        decoded_token = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return decoded_token if decoded_token["exp"] >= time.time() else None

    @staticmethod
    async def get_user_from_token_payload(db_session: AsyncSession, payload: dict) -> Optional[User]:
        user_id = payload['user_id']
        return await crud.get(db_session, user_id)

    async def get_user_from_token(self, db_session: AsyncSession, token: str) -> Optional[User]:
        payload = self.decode_token(token)
        user = await self.get_user_from_token_payload(db_session, payload)
        return user
