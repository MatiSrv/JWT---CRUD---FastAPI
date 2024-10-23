from configs.database import Base
from sqlalchemy import Column, String, Integer


class Song(Base):
    __tablename__ = "songs"
    
    id = Column(Integer, primary_key = True, autoincrement = True)
    title = Column(String)
    artist = Column(String)
    album = Column(String)
    year = Column(Integer)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)