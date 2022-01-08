from sqlmodel import SQLModel, Field


class BaseUserModel(SQLModel):
    first_name: str = Field(nullable=True, default=None)
    last_name: str = Field(nullable=True, default=None)
    username: str = Field(nullable=False, min_length=3, max_length=100)
    email: str = Field(nullable=False, min_length=3, max_length=100)  # TODO: Добавить проверку почты по регулярке


class User(BaseUserModel, table=True):
    id: int = Field(primary_key=True, index=True)
    hashed_password: str = Field(nullable=False)


