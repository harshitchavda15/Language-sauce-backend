from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import JSON  
from database.session import Base

class Snippet(Base):
    __tablename__ = "snippets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)  # New field
    code = Column(String(5000), nullable=False)  # New field
    language = Column(String(50), nullable=False)  # New field
    tags = Column(String(255), nullable=True)  # New field as a comma-separated string
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="snippets")
