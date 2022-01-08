import time
from typing import Optional

import jwt
from fastapi import Header
from sqlmodel.ext.asyncio.session import AsyncSession

from settings import core as settings
from users.models import User
from users.crud import crud


class JWTAuthService:
    @staticmethod
    def gen_token(user: User) -> str:
        user_id = user.id
        payload = {
            'expires': time.time() + settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES,
            'user_id': user_id,
        }
        return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

    @staticmethod
    def decode_token(token: str) -> dict:
        decoded_token = jwt.decode(token, settings.JWT_SECRET, algorithm=[settings.JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None

    @staticmethod
    async def get_user_from_token_payload(db_session: AsyncSession, payload: dict) -> Optional[User]:
        user_id = payload['user_id']
        return await crud.get(db_session, user_id)

    async def get_user_from_token(self, db_session: AsyncSession, token: str) -> Optional[User]:
        payload = self.decode_token(token)
        user = await self.get_user_from_token_payload(db_session, payload)
        return user
