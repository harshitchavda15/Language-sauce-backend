from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.user_model import User  
from schemas.user_schema import UserCreate
from auth.auth import hash_password
import logging

async def create_user(session: AsyncSession, user: UserCreate):
    try:
        # Hash the user's password
        hashed_password = hash_password(user.password)
        
        # Create a new User instance
        db_user = User(
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            hashed_password=hashed_password,
        )
        
        # Add the user to the database
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)
        
        logging.info(f"User created successfully: {user.username}")
        return db_user
    
    except Exception as e:
        await session.rollback()
        logging.error(f"Error creating user: {e}")
        raise e

async def get_user_by_username(session: AsyncSession, username: str):
    try:
        # Execute query to find user by username
        result = await session.execute(select(User).filter(User.username == username))
        user = result.scalars().first()
        
        if user:
            logging.info(f"User found: {username}")
        else:
            logging.warning(f"User not found: {username}")
        
        return user
    
    except Exception as e:
        logging.error(f"Error fetching user by username: {e}")
        raise e
