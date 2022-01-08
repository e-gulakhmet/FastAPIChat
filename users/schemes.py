from sqlmodel import Field, SQLModel

from users.models import BaseUserModel


class UserCreateSchema(BaseUserModel):
    password: str = Field(nullable=False)


class UserUpdateSchema(BaseUserModel):
    email = None


class UserGetSchema(BaseUserModel):
    pass


class UserLoginSchema(SQLModel):
    email: str = Field(nullable=False)
    password: str = Field(nullable=False)
