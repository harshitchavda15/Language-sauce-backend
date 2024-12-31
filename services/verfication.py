import random
import string
import secrets
from datetime import datetime, timedelta
from fastapi_mail import FastMail, MessageSchema
from utils.email import send_email
from config import Settings

# Temporary in-memory OTP storage (for example purposes)
otp_storage = {}

class OTPService:
    def __init__(self, email: str, email_sender=send_email):
        self.email = email
        self.email_sender = email_sender
        self.expiration_time = datetime.utcnow() + timedelta(minutes=Settings.OTP_EXPIRATION_MINUTES or 5)

    def generate_otp(self):
        otp = ''.join(secrets.choice(string.digits) for _ in range(6))
        otp_storage[self.email] = {"otp": otp, "expiration_time": self.expiration_time}
        return otp

    def is_otp_valid(self, provided_otp: str):
        if self.email not in otp_storage:
            return False, "OTP not found"
        stored_otp = otp_storage[self.email]
        if datetime.utcnow() > stored_otp["expiration_time"]:
            return False, "OTP expired"
        if provided_otp != stored_otp["otp"]:
            return False, "Invalid OTP"
        return True, "OTP is valid"

    async def send_otp_email(self):
        otp = self.generate_otp()
        try:
            message = MessageSchema(
                subject="Your OTP Code",
                recipients=[self.email],
                body=f"Your OTP code is: {otp}",
                subtype="plain"
            )
            await self.email_sender(message)
            return {"status": "success", "message": "OTP sent successfully"}
        except Exception as e:
            raise ValueError(f"Failed to send email: {e}")
