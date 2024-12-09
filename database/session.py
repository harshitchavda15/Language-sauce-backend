from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://postgres:1234@localhost:5432/LS"

engine= create_async_engine(DATABASE_URL,echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, autoflush=False, autocommit=False)

def getsession():
    with SessionLocal as session:
        yield session