import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

class Settings:
    # Ensure that environment variables are loaded properly
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:1507@localhost/ls")
    SECRET_KEY = os.getenv("SECRET_KEY", "sjZCOBLiAYcNj-xsN6xX1eNEqIccUKP7LJNhC-iZOOI")
    ALGORITHM = "HS256"  # This is likely correct for JWT tokens (if you're using JWTs)
    ACCESS_TOKEN_EXPIRE_MINUTES = 60  # Expiration time for the access token

    # Optional: Check if important values are missing and raise errors
    def __init__(self):
        if not self.DATABASE_URL:
            raise ValueError("DATABASE_URL is not set in the environment variables.")
        if not self.SECRET_KEY:
            raise ValueError("SECRET_KEY is not set in the environment variables.")

# Example usage
settings = Settings()
print(settings.DATABASE_URL)
print(settings.SECRET_KEY)
