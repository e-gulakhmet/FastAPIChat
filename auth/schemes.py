from typing import Optional

from pydantic import BaseModel


class CredentialsSchema(BaseModel):
    username: Optional[str]
    email: Optional[str]
    password: str


class JWTToken(BaseModel):
    access_token: str
