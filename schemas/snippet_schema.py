from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Schema for creating a snippet
class SnippetCreate(BaseModel):
    title: str
    description: Optional[str] = None
    code: str
    language: str
    tags: Optional[List[str]] = []

    class Config:
        orm_mode = True


# Schema for updating a snippet
class SnippetUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    code: Optional[str] = None
    language: Optional[str] = None
    tags: Optional[List[str]] = None  # Changed default to `None`

    class Config:
        orm_mode = True


# Schema for snippet response
class SnippetResponse(BaseModel):
    id: int  # Changed to `int` if the database uses integers
    title: str
    description: Optional[str]
    code: str
    language: str
    tags: Optional[List[str]]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
