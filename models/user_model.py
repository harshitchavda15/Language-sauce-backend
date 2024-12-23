from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Unique username
    username = Column(String(50), unique=True, index=True, nullable=False)
    
    # Unique email
    email = Column(String(255), unique=True, index=True, nullable=False)
    
    # Full name of the user
    full_name = Column(String(255), nullable=True)
    
    # Hashed password for authentication
    hashed_password = Column(String(255), nullable=False)
    
    # Timestamp for when the user was created
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Timestamp for when the user was last updated
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship to snippets (if applicable)
    snippets = relationship("Snippet", back_populates="author")  # Adjust if Snippet model exists

class OTP(Base):
    __tablename__ = "otps"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    otp = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def is_expired(self):
        return self.created_at < datetime.utcnow() - timedelta(minutes=5)