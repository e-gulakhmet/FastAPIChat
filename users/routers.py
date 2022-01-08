from typing import Any

from fastapi import Depends, APIRouter, HTTPException, Body
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette import status
from starlette.responses import JSONResponse

from auth.auth import get_current_user
from users.crud import crud
from core import db
from users.models import UserCreate, User, UserGet
from auth.services import JWTAuthService

from users.models import UserLogin
from users.services import UserService

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserGet)
async def create_user(data: UserCreate = Body(...), db_session: AsyncSession = Depends(db.get_session)) -> User:
    user = await crud.create(db_session=db_session, obj=data)
    return user


@router.post("/login")
async def login(db_session: AsyncSession = Depends(db.get_session), data: UserLogin = Body(...)) -> Any:
    exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
            )

    user = await crud.get_by_email(db_session, data.email)
    if not user:
        raise exception

    if not (await UserService.verify_password(data.password, user.hashed_password)):
        raise exception

    access_token = JWTAuthService().gen_user_token(user)

    token = jsonable_encoder(access_token)

    response = JSONResponse(content={"access_token": access_token})
    response.headers.append("Authorization", f"Bearer {token}")

    return response


# @router.post("/usernamelogin")
# async def login(db_session: AsyncSession = Depends(db.get_session), user: OAuth2PasswordRequestForm = Depends()) -> Any:
#     user = await crud.get_by_username(db_session, user.username)
#
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect email or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#
#     access_token = JWTAuthService().gen_user_token(user)
#
#     token = jsonable_encoder(access_token)
#     content = {"message": "You've successfully logged in. Welcome back!"}
#     response = JSONResponse(content=content)
#     response.set_cookie(
#         "Authorization",
#         value=f"Bearer {token}",
#         httponly=True,
#         max_age=1800,
#         expires=1800,
#         samesite="Lax",
#         secure=False,
#     )
#
#     return response


@router.get('/me', dependencies=[Depends(get_current_user)], response_model=UserGet)
async def retrieve_me(user: User = Depends(get_current_user)) -> User:
    return user
