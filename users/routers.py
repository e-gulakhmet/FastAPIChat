from fastapi import Depends, APIRouter, Body
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette import status

from auth.auth import get_current_user
from core import db
from users.schemes import UserCreateSchema, UserGetSchema

from users.models import User
from users.crud import crud


router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserGetSchema)
async def create_user(data: UserCreateSchema = Body(...), db_session: AsyncSession = Depends(db.get_session)) -> User:
    user = await crud.create(db_session=db_session, obj=data)
    return user


@router.get(
    '/me',
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_user)],
    response_model=UserGetSchema
)
async def retrieve_me(user: User = Depends(get_current_user)) -> User:
    return user
