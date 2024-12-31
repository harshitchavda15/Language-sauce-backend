from sqlalchemy import Column, String, Integer, DateTime, Boolean
from sqlalchemy.sql import func
from datetime import datetime, timedelta, timezone
import secrets
from database.session import Base

class OTP(Base):
    __tablename__ = "otps"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True, nullable=False)
    otp = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)
    is_used = Column(Boolean, default=False)
    attempts = Column(Integer, default=0)
    
    MAX_ATTEMPTS = 3  # Configurable attempt limit
    
    @classmethod
    def generate_otp(cls):
        return ''.join(secrets.choice('0123456789') for _ in range(6))
    
    def is_expired(self):
        return datetime.now(timezone.utc) > self.expires_at
    
    def is_valid(self, provided_otp: str):
        return (
            not self.is_expired() and 
            not self.is_used and 
            self.attempts < self.MAX_ATTEMPTS and 
            self.otp == provided_otp
        )
    
    def set_email(self, email: str):
        self.email = email.strip().lower()  # Normalize email
