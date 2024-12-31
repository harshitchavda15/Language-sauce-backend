from pydantic import BaseModel, EmailStr, Field, constr, ValidationError
from typing import Optional

# Create User Schema
class CreateUser(BaseModel):
    email: EmailStr
    full_name: constr(min_length=2, max_length=100) 
    password: constr(min_length=8)                 
    confirm_password: constr(min_length=8)         

    # Custom validation to ensure passwords match
    def validate_passwords(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")

    # Overriding __init__ to call the custom validation
    def __init__(self, **data):
        super().__init__(**data)
        self.validate_passwords()

    class Config:
        orm_mode = True


# Sign-In Schema
class SignInRequest(BaseModel):
    email: EmailStr = Field(..., example="chavda@example.com")
    fullname: str = Field(..., example="Chavda Harshit")
    password: str = Field(..., example="password@123")
    confirm_password: str = Field(..., example="password@123")

    # Custom validation to ensure passwords match
    def validate_passwords(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")

    def __init__(self, **data):
        super().__init__(**data)
        self.validate_passwords()

    class Config:
        orm_mode = True


# User Response Schema
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: Optional[str]

    class Config:
        orm_mode = True


# User Login Schema
class UserLogin(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True
