from typing import Any

from fastapi import Request, Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette import status

from crud.users import crud
import db
from models.users import UserCreate, User, UserGet
from services.auth import JWTAuthService

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserGet)
async def create_user(request_data: UserCreate, db_session: AsyncSession = Depends(db.get_session)) -> User:
    """ Create new user """

    print(request_data)

    user = await crud.create(db=db_session, obj_in=request_data)
    return user


# Добавить response body и request body
@router.post("/login")
async def login(db_session: AsyncSession = Depends(db.get_session), form_data: OAuth2PasswordRequestForm = Depends()
                ) -> Any:
    """ Get the JWT for a user with data from OAuth2 request form body. """

    user = await JWTAuthService.authenticate(email=form_data.username, password=form_data.password, db=db_session)  # 2
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")  # 3

    return {
        "access_token": await JWTAuthService().create_access_token(sub=str(user.id)),  # 4
        "token_type": "bearer",
    }