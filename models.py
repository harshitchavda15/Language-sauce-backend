from sqlalchemy import Column,String,Integer,DateTime
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    
    __tablename__="users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)