from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from core.crud import CRUDBase

from users.models import User
from users.schemes import UserCreateSchema, UserUpdateSchema
from users.services import UserService


class CRUDUser(CRUDBase[User, UserCreateSchema, UserUpdateSchema]):
    async def create(self, db_session: AsyncSession, *, obj: UserCreateSchema) -> User:
        obj_data = obj.dict()
        obj_data.pop("password")
        db_obj = User(**obj_data)
        db_obj.hashed_password = await UserService.hash_password(obj.password)
        db_session.add(db_obj)
        await db_session.commit()
        return db_obj

    @staticmethod
    async def get_by_email(db_session: AsyncSession, email: str) -> User:
        return (await db_session.execute(select(User).where(User.email == email))).scalar()

    @staticmethod
    async def get_by_username(db_session: AsyncSession, username: str) -> User:
        return (await db_session.execute(select(User).where(User.username == username))).scalar()


crud = CRUDUser(User)
