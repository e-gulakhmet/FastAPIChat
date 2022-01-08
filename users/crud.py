from sqlmodel.ext.asyncio.session import AsyncSession

from core.crud import CRUDBase
from models.users import User, UserCreate, UserUpdate
from services.users import UserService


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def create(self, db_session: AsyncSession, *, obj: UserCreate) -> User:
        obj_data = obj.dict()
        obj_data.pop("password")
        db_obj = User(**obj_data)
        db_obj.hashed_password = await UserService.hash_password(obj.password)
        db_session.add(db_obj)
        await db_session.refresh(db_obj)
        await db_session.commit()
        return db_obj


crud = CRUDUser(User)
