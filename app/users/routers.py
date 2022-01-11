from typing import List

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.auth.auth import get_current_user
from app.users.models import User
from app.users.schemes import UserOutScheme, UserCreateScheme, UserUpdateScheme

router = APIRouter(prefix='/users', tags=['users'])


@router.get("/", response_model=List[UserOutScheme], status_code=status.HTTP_200_OK)
async def read_users(skip: int = 0, limit: int = 100, current_user: User = Depends(get_current_user)):
    """ Users list """
    users = await User.all().limit(limit).offset(skip)
    return users


@router.post("/", response_model=UserOutScheme, status_code=status.HTTP_201_CREATED)
async def create_user(*, user_obj: UserCreateScheme):
    """Create new user."""
    if await User.get_by_email(email=user_obj.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this email already exists in the system.",
        )

    user = await User.create(user_obj)

    return user


@router.put("/me", response_model=UserOutScheme, status_code=status.HTTP_200_OK)
async def update_user_me(user_obj: UserUpdateScheme, current_user: User = Depends(get_current_user)):
    """ Update own user. """
    user_to_update = current_user
    if user_obj.username is not None:
        user_to_update.username = user_obj.username
    if user_obj.first_name is not None:
        user_to_update.first_name = user_obj.first_name
    if user_obj.last_name is not None:
        user_to_update.last_name = user_obj.last_name
    await user_to_update.save()
    return user_to_update


@router.get("/me", response_model=UserOutScheme, status_code=status.HTTP_200_OK)
def read_user_me(current_user: User = Depends(get_current_user)):
    """ Get current user """
    return current_user


@router.get("/{user_id}", response_model=UserOutScheme, status_code=status.HTTP_200_OK)
async def read_user_by_id(user_id: int, current_user: User = Depends(get_current_user)):
    """ Get a specific user by id. """
    user = await User.get(id=user_id)
    return user
