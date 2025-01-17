from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional

# Create User Schema
class CreateUser(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str  # Temporary field for validation
    fullname: str
    mobile_number: Optional[str] = None

    # Custom validation to ensure passwords match
    @validator("confirm_password")
    def passwords_match(cls, confirm_password, values):
        if "password" in values and confirm_password != values["password"]:
            raise ValueError("Passwords do not match")
        return confirm_password

    class Config:
        orm_mode = True


# Sign-In Schema
class SignInRequest(BaseModel):
    email: EmailStr = Field(..., example="chavda@example.com")
    password: str = Field(..., example="password@123")

    class Config:
        orm_mode = True


# User Response Schema
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    fullname: Optional[str]
    mobile_number: Optional[str]

    class Config:
        orm_mode = True


# User Login Schema (if username-based login is used)
class UserLogin(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True
