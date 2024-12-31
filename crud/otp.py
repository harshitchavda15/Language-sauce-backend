import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta
from models.otp_models import OTP
from fastapi import HTTPException

# Constants
OTP_EXPIRY_MINUTES = 5
MAX_ATTEMPTS = 3

# Logger setup
logger = logging.getLogger(__name__)

async def create_otp(db: AsyncSession, email: str) -> OTP:
    email = email.strip().lower()  # Normalize email
    logger.info(f"Creating OTP for email: {email}")
    
    # Delete any existing OTP for this email
    stmt = select(OTP).where(OTP.email == email)
    result = await db.execute(stmt)
    existing_otp = result.scalar_one_or_none()
    
    if existing_otp:
        await db.delete(existing_otp)
    
    new_otp = OTP(
        email=email,
        otp=OTP.generate_otp(),
        expires_at=datetime.utcnow() + timedelta(minutes=OTP_EXPIRY_MINUTES)
    )
    db.add(new_otp)
    await db.commit()
    await db.refresh(new_otp)
    
    logger.info(f"OTP created for email: {email}, OTP: {new_otp.otp}")
    return new_otp

async def verify_otp(db: AsyncSession, email: str, otp_code: str) -> bool:
    email = email.strip().lower()  # Normalize email
    logger.info(f"Verifying OTP for email: {email}")
    
    stmt = select(OTP).where(
        OTP.email == email,
        OTP.is_used == False
    ).order_by(OTP.created_at.desc())
    
    result = await db.execute(stmt)
    otp_record = result.scalar_one_or_none()
    
    if not otp_record:
        logger.warning(f"OTP not found for email: {email}")
        raise HTTPException(status_code=404, detail="OTP not found")
    
    otp_record.attempts += 1
    
    if otp_record.attempts >= MAX_ATTEMPTS:
        logger.warning(f"Too many attempts for email: {email}")
        raise HTTPException(status_code=400, detail="Too many attempts")
    
    if otp_record.is_expired():
        logger.warning(f"Expired OTP for email: {email}")
        raise HTTPException(status_code=400, detail="OTP has expired")
    
    if otp_record.otp != otp_code:
        await db.commit()
        logger.warning(f"Invalid OTP for email: {email}")
        raise HTTPException(status_code=400, detail="Invalid OTP")
    
    otp_record.is_used = True
    await db.commit()
    logger.info(f"OTP verified successfully for email: {email}")
    return True
