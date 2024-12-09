from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from models.snippet import Snippet
from schemas.snippet import SnippetCreate

# Create a new snippet
async def create_snippet(session: AsyncSession, title: str, content: str, user_id: int) -> Snippet:
    try:
        snippet = Snippet(title=title, content=content, user_id=user_id)
        session.add(snippet)
        await session.commit()
        await session.refresh(snippet)
        return snippet
    except SQLAlchemyError as e:
        await session.rollback()
        raise e  # Re-raise the exception for logging or debugging

# Get all snippets
async def get_all_snippet(session: AsyncSession):
    try:
        result = await session.execute(select(Snippet))
        return result.scalars().all()  # Returns a list of Snippet objects
    except SQLAlchemyError as e:
        raise e

# Delete a snippet by ID
async def delete_snippet(session: AsyncSession, snippet_id: int) -> bool:
    try:
        result = await session.execute(select(Snippet).filter(Snippet.id == snippet_id))
        snippet = result.scalars().first()  # Use `.first()` to get a single object

        if snippet is None:
            return False  # Snippet not found
        
        await session.delete(snippet)  # Delete the retrieved Snippet object
        await session.commit()
        return True  # Successfully deleted
    except SQLAlchemyError as e:
        await session.rollback()  # Rollback on error
        raise e
