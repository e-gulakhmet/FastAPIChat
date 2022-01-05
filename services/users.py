from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlmodel.ext.asyncio.session import AsyncSession
from jose import jwt

from models.users import User
from settings import core as settings
import db

PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    oauth2_schemeoauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"/auth/login")

    @staticmethod
    async def verify_password(plain_password: str, hashed_password: str) -> bool:
        return PWD_CONTEXT.verify(plain_password, hashed_password)

    @staticmethod
    async def hash_password(password) -> str:
        return PWD_CONTEXT.hash(password)

    @staticmethod
    async def get_current_user(db_session: AsyncSession = Depends(db.get_session), token: str = Depends(oauth2_scheme)
                               ) -> User:
        try:
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.ALGORITHM],
                                 options={"verify_aud": False})
            username: str = payload.get("sub")
            token_data = TokenData(username=username)
        except JWTError:
            raise credentials_exception
        user = db_session.query(User).filter(User.id == token_data.username).first()
        if user is None:
            raise credentials_exception
        return user
