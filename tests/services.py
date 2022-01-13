from app.users.models import User
from app.users.schemes import UserCreateScheme
from app.utils.random import random_string


class TestDataService:
    USER_PASSWORD = 'Test12345'

    async def create_user(self) -> User:
        return await User.create(UserCreateScheme(email=f'{random_string(6)}@test.com', password=self.USER_PASSWORD))
