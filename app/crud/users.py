from app.crud.base import CRUDBase
from app.models.users import User
from app.schemas.users import UserCreate, UserUpdate


class CRUDRecipe(CRUDBase[User, UserCreate, UserUpdate]):
    ...


recipe = CRUDRecipe(User)
