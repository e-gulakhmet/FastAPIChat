from typing import Optional

from pydantic import BaseModel, EmailStr


class BaseUserScheme(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    is_superuser: Optional[bool] = False


class UserDBScheme(BaseUserScheme):
    id: int
    password_hash: str

    class Config:
        orm_mode = True


class UserOutScheme(BaseUserScheme):
    id: int

    class Config:
        orm_mode = True


class UserCreateScheme(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: EmailStr
    username: Optional[str] = None
    password: str


class UserUpdateScheme(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]