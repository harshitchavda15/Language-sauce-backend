from pydantic import BaseModel
from typing import Optional,List
from uuid import UUID

class SnippetBase(BaseModel):
    title: str
    description: Optional[str] = None
    code: str
    language: str
    tags: Optional[List[str]] = []
    dfficulty: Optional[str] = None

class SnippetCreate(SnippetBase):
    pass

class Snippet(SnippetBase):
    id: UUID
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True