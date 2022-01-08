from fastapi import Header
from sqlmodel.ext.asyncio.session import AsyncSession

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette import status

from auth.services import JWTAuthService
from users.models import User


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = JWTAuthService.decode_token(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid


async def get_request_user(db_session: AsyncSession, token: str = Header(...)) -> User:
    user = await JWTAuthService().get_user_from_token(db_session, token)
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return user
