from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    hashed_password: str = Field(nullable=False)
    first_name: str = Field(nullable=True, default=None)
    last_name: str = Field(nullable=True, default=None)
    username: str = Field(nullable=True, default=None, min_length=3, max_length=100)
    email: str = Field(nullable=False, min_length=3, max_length=100)  # TODO: Добавить проверку почты по регулярке


