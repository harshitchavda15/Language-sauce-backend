from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database.session import get_db
from schemas.otp import OTPCreate, OTPVerify, OTPResponse
from crud.otp import create_otp, verify_otp
from utils.email import send_email
from pydantic import BaseModel

router = APIRouter()

class OTPVerifyResponse(BaseModel):
    message: str

@router.post("/otp/generate", response_model=OTPResponse)
async def generate_otp(
    request: OTPCreate,
    db: AsyncSession = Depends(get_db)
):
    otp = await create_otp(db, request.email)
    try:
        # Send OTP via email
        await send_email(request.email, otp.otp)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to send OTP. Please try again later."
        )
    return OTPResponse(
        message="OTP sent successfully",
        expires_at=otp.expires_at
    )

@router.post("/otp/verify", response_model=OTPVerifyResponse)
async def verify_otp_route(
    request: OTPVerify,
    db: AsyncSession = Depends(get_db)
):
    is_valid = await verify_otp(db, request.email, request.otp)
    if is_valid:
        return {"message": "OTP verified successfully"}
    raise HTTPException(
        status_code=400,
        detail="Invalid OTP or OTP has expired."
    )
