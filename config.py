import os 

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL","postgresql+asyncpg://user:password@localhost/dbname")
    SECRET_KEY= os.getenv("SECRET_KEY", "sjZCOBLiAYcNj-xsN6xX1eNEqIccUKP7LJNhC-iZOOI")
    ALGORITHM= "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES= 60
