from passlib.context import CryptContext

PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    @staticmethod
    async def verify_password(plain_password: str, hashed_password: str) -> bool:
        return PWD_CONTEXT.verify(plain_password, hashed_password)

    @staticmethod
    async def hash_password(password) -> str:
        return PWD_CONTEXT.hash(password)
