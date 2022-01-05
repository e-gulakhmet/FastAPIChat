from typing import Optional, MutableMapping, List, Union
from datetime import datetime, timedelta
from jose import jwt

from sqlmodel.ext.asyncio.session import AsyncSession

from settings import core as settings
from models.users import User
from services.users import UserService


class JWTAuthService:
    JWTPayloadMapping = MutableMapping[str, Union[datetime, bool, str, List[str], List[int]]]

    @staticmethod
    async def authenticate(*, email: str, password: str, db: AsyncSession) -> Optional[User]:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return None
        if not UserService().verify_password(password, user.hashed_password):  # 1
            return None
        return user

    async def create_access_token(self, *, sub: str) -> str:  # 2
        return await self._create_token(
            token_type="access_token",
            lifetime=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),  # 3
            sub=sub,
        )

    @staticmethod
    async def _create_token(token_type: str, lifetime: timedelta, sub: str) -> str:
        payload = {}
        expire = datetime.utcnow() + lifetime
        payload["type"] = token_type
        payload["exp"] = expire  # 4
        payload["iat"] = datetime.utcnow()  # 5
        payload["sub"] = str(sub)  # 6

        return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)  # 8
