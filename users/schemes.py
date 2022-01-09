from sqlmodel import Field, SQLModel


class UserCreateSchema(SQLModel):
    email: str = Field(nullable=False)
    password: str = Field(nullable=False)


class UserUpdateSchema(SQLModel):
    first_name: str = Field(nullable=True, default=None)
    last_name: str = Field(nullable=True, default=None)
    username: str = Field(nullable=False, min_length=3, max_length=100)


class UserGetSchema(SQLModel):
    id: int
    first_name: str
    last_name: str
    username: str
    email: str


class UserLoginSchema(SQLModel):
    email: str = Field(nullable=False)
    password: str = Field(nullable=False)
