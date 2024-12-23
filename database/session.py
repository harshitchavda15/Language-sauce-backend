from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base  # Correct import for Base
from dotenv import load_dotenv
import os
import logging

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:1507@localhost:5432/ls")

# Create a declarative base instance for models to inherit from
Base = declarative_base()

# Create the async engine
engine = create_async_engine(DATABASE_URL, echo=os.getenv("SQL_ECHO", "False") == "True")

# Create an asynchronous session factory
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False
)

# Dependency to get a database session (async context)
async def get_session():
    try:
        async with SessionLocal() as session:
            yield session
    except Exception as e:
        logging.error(f"Database session error: {e}")
        raise
    