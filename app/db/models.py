from sqlalchemy import Column, Integer, String, Boolean
from app.db.database import Base


class VM(Base):
    __tablename__ = "vms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    status = Column(String)
    cpu = Column(Integer)
    memory = Column(Integer)
    os = Column(String)
    region = Column(String)
    owner = Column(String)
    is_active = Column(Boolean, default=True)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)