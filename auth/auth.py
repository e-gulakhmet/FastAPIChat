from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from sqlmodel.ext.asyncio.session import AsyncSession

from auth.services import JWTAuthService
from core import db
from users.models import User

security = OAuth2PasswordBearer(tokenUrl="/users/login")


async def get_current_user(db_session: AsyncSession = Depends(db.get_session), token: str = Depends(security)) -> User:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    user = await JWTAuthService().get_user_from_token(db_session, token)
    if not user:
        raise credentials_exception

    return user
