from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.snippet_schema import SnippetCreate, SnippetResponse
from crud.snippet_crud import create_snippet, get_all_snippets, get_snippet, delete_snippet
from database.session import get_session  # Dependency to get the database session

router = APIRouter()

# Create a new snippet
@router.post("/snippets", response_model=SnippetResponse)
async def create_snippet_endpoint(
    snippet: SnippetCreate, 
    session: AsyncSession = Depends(get_session)
):
    try:
        return await create_snippet(session, snippet)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create snippet: {e}")

# Get all snippets
@router.get("/snippets", response_model=list[SnippetResponse])
async def get_all_snippets_endpoint(session: AsyncSession = Depends(get_session)):
    try:
        return await get_all_snippets(session)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve snippets: {e}")

# Get a snippet by ID
@router.get("/snippets/{snippet_id}", response_model=SnippetResponse)
async def get_snippet_endpoint(
    snippet_id: str, 
    session: AsyncSession = Depends(get_session)
):
    snippet = await get_snippet(session, snippet_id)
    if not snippet:
        raise HTTPException(status_code=404, detail="Snippet not found")
    return snippet

# Delete a snippet by ID
@router.delete("/snippets/{snippet_id}", response_model=dict)
async def delete_snippet_endpoint(
    snippet_id: str, 
    session: AsyncSession = Depends(get_session)
):
    success = await delete_snippet(session, snippet_id)
    if not success:
        raise HTTPException(status_code=404, detail="Snippet not found")
    return {"message": "Snippet deleted successfully"}
