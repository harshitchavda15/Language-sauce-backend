from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from models.snippet import Snippet
from schemas.snippet import SnippetCreate
import logging

# Create a new snippet
async def create_snippet(session: AsyncSession, snippet_data: SnippetCreate, user_id: int) -> Snippet:
    """
    Creates a new snippet in the database.
    
    Args:
        session: Database session.
        snippet_data: SnippetCreate schema containing title and content.
        user_id: ID of the user creating the snippet.

    Returns:
        The created Snippet object.
    """
    try:
        snippet = Snippet(
            title=snippet_data.title,
            content=snippet_data.content,
            language=snippet_data.language,
            tags=snippet_data.tags,
            author_id=user_id
        )
        session.add(snippet)
        await session.commit()
        await session.refresh(snippet)
        logging.info(f"Snippet created successfully with ID: {snippet.id}")
        return snippet
    except SQLAlchemyError as e:
        await session.rollback()
        logging.error(f"Error creating snippet: {e}")
        raise e

# Get all snippets
async def get_all_snippets(session: AsyncSession) -> list[Snippet]:
    """
    Retrieves all snippets from the database.
    
    Args:
        session: Database session.

    Returns:
        A list of Snippet objects.
    """
    try:
        result = await session.execute(select(Snippet))
        snippets = result.scalars().all()
        logging.info(f"Retrieved {len(snippets)} snippets.")
        return snippets
    except SQLAlchemyError as e:
        logging.error(f"Error fetching snippets: {e}")
        raise e

# Delete a snippet by ID
async def delete_snippet(session: AsyncSession, snippet_id: int) -> bool:
    """
    Deletes a snippet by its ID.
    
    Args:
        session: Database session.
        snippet_id: ID of the snippet to delete.

    Returns:
        True if the snippet was deleted successfully, False otherwise.
    """
    try:
        result = await session.execute(select(Snippet).filter(Snippet.id == snippet_id))
        snippet = result.scalars().first()

        if snippet is None:
            logging.warning(f"Snippet with ID {snippet_id} not found.")
            return False
        
        await session.delete(snippet)
        await session.commit()
        logging.info(f"Snippet with ID {snippet_id} deleted successfully.")
        return True
    except SQLAlchemyError as e:
        await session.rollback()
        logging.error(f"Error deleting snippet with ID {snippet_id}: {e}")
        raise e
