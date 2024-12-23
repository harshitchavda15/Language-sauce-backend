from sqlalchemy import Column, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, ARRAY  # Use ARRAY for PostgreSQL array type
from sqlalchemy.ext.declarative import declarative_base
import uuid
from datetime import datetime

Base = declarative_base()

class Snippet(Base):
    __tablename__ = 'snippets'
    
    # UUID for the snippet ID
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Title of the snippet
    title = Column(String(255), nullable=False)
    
    # Optional description for the snippet
    description = Column(Text, nullable=True)  # Explicitly set nullable
    
    # The actual code for the snippet
    code = Column(Text, nullable=False)
    
    # Language of the snippet (e.g., Python, JavaScript)
    language = Column(String(50), nullable=False, index=True)  # Add indexing for search
    
    # Tags for the snippet (e.g., ['algorithm', 'sorting'])
    tags = Column(ARRAY(String(50)), nullable=True, index=True)  # Add indexing for search
    
    # Timestamp when the snippet was created
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    
    # Timestamp when the snippet was last updated
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign key to the user who authored the snippet
    author_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    
    # Relationship to the User model (if you have a User model)
    author = relationship("User", back_populates="snippets")
