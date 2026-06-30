from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class File(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    path = Column(String)
    size = Column(Float)

class Block(Base):
    __tablename__ = "blocks"
    id = Column(Integer, primary_key=True)
    file_id = Column(Integer)
    stored_in = Column(Integer)
