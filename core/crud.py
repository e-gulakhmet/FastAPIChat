from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=SQLModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=SQLModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        :param model: A SQLModel model class
        """

        self.model = model

    async def get(self, db_session: AsyncSession, id: int) -> Optional[ModelType]:
        return db_session.query(self.model).filter(self.model.id == id).first()

    async def get_multi(self, db_session: AsyncSession, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        return db_session.query(self.model).offset(skip).limit(limit).all()

    async def create(self, db_session: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db_session.add(db_obj)
        await db_session.commit()
        await db_session.refresh(db_obj)
        return db_obj

    async def update(self, db_session: AsyncSession, *, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]
                     ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db_session.add(db_obj)
        await db_session.commit()
        await db_session.refresh(db_obj)
        return db_obj

    async def remove(self, db_session: AsyncSession, *, id: int) -> ModelType:
        obj = db_session.query(self.model).get(id)
        await db_session.delete(obj)
        await db_session.commit()
        return obj
