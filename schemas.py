from pydantic import BaseModel
from typing import optional

class UserCreate(BaseModel):
    username: str
    email: str
    full_name: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: str

class UserLogin(BaseModel):
    username: str
    password: str