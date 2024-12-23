from fastapi.mail import FastMail, MessageSchema, ConnectionConfig
from config import Settings

# Set up your email configuration
conf = ConnectionConfig(
    MAIL_USERNAME="your_email@example.com",
    MAIL_PASSWORD="your_password",
    MAIL_FROM="your_email@example.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.example.com",
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

# Function to send an email
async def send_email(message: MessageSchema):
    fm = FastMail(conf)
    await fm.send_message(message)
