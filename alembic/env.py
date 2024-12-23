from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context
import asyncio

# Import your Base (all models) from the backend project structure
from models import Base  # Ensure this matches your actual `Base` location

# Load the `.env` file to get the database URL dynamically
from dotenv import load_dotenv
import os

load_dotenv()

# Get the DATABASE_URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:1507@localhost:5432/ls")

# This is the Alembic Config object
config = context.config

# Set the database URL dynamically in the Alembic configuration
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Interpret the config file for Python logging
fileConfig(config.config_file_name)

# Add your project's metadata for 'autogenerate' support
target_metadata = Base.metadata

def run_migrations_online():
    """Run migrations in 'online' mode."""
    # Create the async engine for the database connection
    connectable = create_async_engine(DATABASE_URL, poolclass=pool.NullPool)

    # Function to perform migrations and schema inspection
    async def do_migration():
        async with connectable.connect() as connection:
            # Run Alembic configuration with sync context
            await connection.run_sync(lambda conn: context.configure(connection=conn, target_metadata=target_metadata))

            # Perform migration
            async with connection.begin():
                await context.run_migrations()

    # Run the migrations
    asyncio.run(do_migration())

# Execute the migration runner
run_migrations_online()
