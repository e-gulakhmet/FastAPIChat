from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from app.auth.schemes import JWTToken, CredentialsSchema
from app.auth.services import JWTAuthService, AuthService
from app.users.models import User

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post("/access-token", response_model=JWTToken)
async def login_access_token(credentials: CredentialsSchema):
    user = await AuthService(User).auth(credentials)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    token = jsonable_encoder(JWTAuthService(User).gen_user_token(user))
    response = JSONResponse(content={"access_token": f"Bearer {token}"})
    response.headers.append("Authorization", f"Bearer {token}")
    return response
