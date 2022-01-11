from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.auth.services import JWTAuthService
from app.users.models import User

security = OAuth2PasswordBearer(tokenUrl="/auth/access-token")


async def get_current_user(token: str = Depends(security)) -> User:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    user = await JWTAuthService(User).get_user_from_token(token)
    if not user:
        raise credentials_exception

    return user
