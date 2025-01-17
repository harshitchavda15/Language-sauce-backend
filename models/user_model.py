from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from database.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, nullable=False)  # User's email address
    password = Column(String(255), nullable=False)  # User's password
    mobile_number = Column(String(15), nullable=True)  # New column
    fullname = Column(String(100), nullable=False)  # Full name of the user

    snippets = relationship("Snippet", back_populates="user")  # Relationship with Snippet
