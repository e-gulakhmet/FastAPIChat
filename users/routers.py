from typing import Any

from fastapi import Depends, APIRouter, HTTPException, Body
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette import status

from users.crud import crud
import db
from users.models import UserCreate, User, UserGet
from auth.services import JWTAuthService

from users.models import UserLogin
from users.services import UserService
from auth import auth

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserGet)
async def create_user(data: UserCreate = Body(...), db_session: AsyncSession = Depends(db.get_session)) -> User:
    user = await crud.create(db_session=db_session, obj=data)
    return user


@router.post("/login")
async def login(db_session: AsyncSession = Depends(db.get_session), data: UserLogin = Body(...)) -> Any:
    user = await crud.get_by_email(db_session, data.email)
    if not UserService.verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail='Incorrect email or password')

    return {
        "access_token": JWTAuthService().gen_token(user),  # 4
        "token_type": "bearer",
    }


@router.get('/me', dependencies=[Depends(auth.JWTBearer())], response_model=UserGet)
async def retrieve_me(user: User = Depends(auth.get_request_user)) -> User:
    return user
