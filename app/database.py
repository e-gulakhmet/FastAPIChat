from typing import Dict

from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import sessionmaker, declared_attr

from app.settings.common import DB_URL

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class_registry: Dict = {}


@as_declarative(class_registry=class_registry)
class Base:
    __name__: str
    id = Column(Integer, primary_key=True, index=True)

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
