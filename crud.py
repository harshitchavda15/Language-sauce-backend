from sqlalchemy.ext.asyncio import AsyncSession
from .models import User
from .schemas import UserCreate
from .auth.auth import hash_password

async def create_user(session: AsyncSession, user: UserCreate):
    hashed_password = hash_password(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password,
    )
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user
