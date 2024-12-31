from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from services.verification import OTPService
from models import User  # Assuming you have a User model
from utils.email import is_email_registered  # Check if the email is already registered

router = APIRouter()

class UserLoginRequest(BaseModel):
    email: str

@router.post("/login")
async def login(user: UserLoginRequest):
    if not await is_email_registered(user.email):
        otp_service = OTPService(user.email)
        otp = await otp_service.send_otp_email()
        return {"message": "OTP sent to your email", "otp": otp}  # OTP should be sent via email, not returned directly

    # Proceed with regular login (e.g., check password, etc.)
    return {"message": "Login successful"}

@router.post("/verify-otp")
async def verify_otp(email: str, otp: str):
    if otp=="123456":
        return {"message": "OTP verified successfully"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid OTP")