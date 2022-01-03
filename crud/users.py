from crud.base import CRUDBase
from models.users import User
from schemas.users import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    ...


recipe = CRUDUser(User)
