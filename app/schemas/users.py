from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserGet(UserBase):
    pass


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    pass


class UserInDB(UserBase):
    hashed_password: str

    class Config:
        orm_mode = True
