from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from database.session import SessionLocal, engine, Base
from config import settings
from crud.user_crud import get_user_by_username
from auth.auth import verify_password, create_access_token
from routes.user import router as user_router
from routes.otp import router as otp_router
from routes.snippet import router as snippet_router
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Access the variables from .env
DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")

# Debug info (REMOVE in production)
if os.getenv("ENV", "development") == "development":
    print("Database URL:", DATABASE_URL)
    print("Secret Key:", SECRET_KEY)

# FastAPI application instance
app = FastAPI(title="LS Backend", version="1.0.0")

# Add CORS middleware
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:5500").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(user_router, prefix="/api/v1/users", tags=["Users"])
app.include_router(otp_router, prefix="/api/v1/otp", tags=["OTP"])
app.include_router(snippet_router, prefix="/api/v1/snippets", tags=["Snippets"])
app.include_router(user_router, prefix="/api/v1/users", tags=["Users"])

@app.get("/")
async def root():
    return {"message": "API is running!"}

# Ensure that the tables are created on startup
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("Tables created successfully!")


# Dependency to get the database session
async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session

# Login endpoint
@app.post("/login", tags=["Authentication"])
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    session: AsyncSession = Depends(get_session)
):
    # Retrieve the user by username
    user = await get_user_by_username(session, form_data.username)

    # If the user doesn't exist or the password is incorrect, raise an exception
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate the access token
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
