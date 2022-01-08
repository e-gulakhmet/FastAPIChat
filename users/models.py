from sqlmodel import SQLModel, Field


class BaseUserModel(SQLModel):
    first_name: str
    last_name: str
    username: str = Field(nullable=False, min_length=3, max_length=100)
    email: str = Field(nullable=False, min_length=3, max_length=100)  # TODO: Добавить проверку почты по регулярке


class User(BaseUserModel, table=True):
    id: int = Field(primary_key=True)
    hashed_password: str = Field(nullable=False)


