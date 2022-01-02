from app.crud.base import CRUDBase
from app.models.users import User
from app.schemas.users import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    ...


recipe = CRUDUser(User)
