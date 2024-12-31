from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from database.session import get_session
from crud.user_crud import get_user_by_email
from auth.auth import verify_password, create_access_token
from schemas.user_schema import SignInRequest
from pydantic import BaseModel, EmailStr

router = APIRouter()

#custom schema for signin
class SignInRequest(BaseModel):
    email: EmailStr 
    password: str
    confirm_password: str
    fullname: str
# Placeholder endpoint
@router.get("/users", tags=["users"])
async def get_users():
    return {"message": "List of users"}

# Sign-In endpoint
@router.post("/sign-in", tags=["Authentication"])
async def sign_in(
    request : SignInRequest,
    session: AsyncSession = Depends(get_session),
):
    user = await get_user_by_email(session, request.email)
    if not user or not verify_password(request.password,request.email):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials"
        )
    # Generate access token
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer","fullname":user.fullname}
