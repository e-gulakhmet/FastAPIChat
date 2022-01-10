from typing import Optional

from sqlmodel import Field, SQLModel


class UserCreateSchema(SQLModel):
    email: str
    password: str


class UserUpdateSchema(SQLModel):
    first_name: Optional[str]
    last_name: Optional[str]
    username: str = Field(nullable=False, min_length=3, max_length=100)


class UserGetSchema(SQLModel):
    id: int
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]
    email: str


class UserLoginSchema(SQLModel):
    email: str
    password: str
