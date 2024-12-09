from sqlalchemy import Column,String,Text,TIMESTAMP,ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import UUID ,array
from sqlalchemy.ext.declarative import declarative_base
import uuid
from datetime import datetime

class Snippet(Base):
    __tablename__ = 'snippets'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    code = Column(Text, nullable=False)
    language = Column(String(50), nullable=False)
    tags = Column(array(String(50)))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    author_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)