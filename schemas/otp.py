from pydantic import BaseModel, EmailStr, validator
from datetime import datetime
from typing import Optional

class OTPCreate(BaseModel):
    email: EmailStr

class OTPVerify(BaseModel):
    email: EmailStr
    otp: str

    @validator("otp")
    def validate_otp(cls, value):
        if len(value) != 6 or not value.isdigit():
            raise ValueError("Invalid OTP. It must be a 6-digit number.")
        return value

class OTPResponse(BaseModel):
    message: str
    expires_at: Optional[datetime]
    is_resend: bool = False
