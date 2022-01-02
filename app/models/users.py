from sqlalchemy import Column, String
from app.database import Base


class User(Base):
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
