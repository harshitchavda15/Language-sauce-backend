from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from database.session import get_session
from crud.user_crud import get_user_by_email
from auth.auth import verify_password, create_access_token
from schemas.user_schema import SignInRequest
from pydantic import BaseModel, EmailStr
from schemas.user_schema import CreateUser
from passlib.context import CryptContext
router = APIRouter()

#custom schema for signin
class SignInRequest(BaseModel):
    email: EmailStr 
    password: str
    confirm_password: str
    fullname: str
    mobile_number: str
# Placeholder endpoint
@router.get("/users", tags=["users"])
async def get_users():
    return {"message": "List of users"}

# Sign-In endpoint
@router.post("/sign-up")
async def sign_up(user: CreateUser, session: AsyncSession = Depends(get_session)):
    # Validate that passwords match
    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    # Hash the password
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = pwd_context.hash(user.password)

    # Create the user
    new_user = CreateUser(
        email=user.email,
        password=hashed_password,
        fullname=user.fullname,
        mobile_number=user.mobile_number
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return {"message": "User created successfully"}

    # Generate access token
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer","fullname":user.fullname}

