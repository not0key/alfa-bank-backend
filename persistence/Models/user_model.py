from sqlalchemy import Column, Integer, String, Boolean
from persistence.database import Base
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    firstName = Column(String)
    lastName = Column(String)
    password = Column(String)
    isActive = Column(Boolean, default=True)
