import random
import string
from datetime import datetime, timedelta
from fastapi.mail import FastMail, MessageSchema
from utils.email import send_email
from config import Settings

class OTPService:
    def __init__(self, email: str):
        self.email = email
        self.expiration_time = datetime.utcnow() + timedelta(minutes=5)  # OTP expires in 5 minutes

    def generate_otp(self):
        otp = ''.join(random.choices(string.digits, k=6))  # Generate a 6-digit OTP
        return otp

    async def send_otp_email(self):
        otp = self.generate_otp()
        message = MessageSchema(
            subject="Your OTP Code",
            recipients=[self.email],
            body=f"Your OTP code is: {otp}",
            subtype="plain"
        )
        await send_email(message)
        return otp
