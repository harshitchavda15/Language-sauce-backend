from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database.session import get_session
from schemas.snippet import SnippetCreate, SnippetResponse
from crud.snippet import create_snippet
from crud.snippet import get_all_snippets

router = APIRouter()

@router.post("/snippets", response_model=SnippetResponse)
async def create_snippet_endpoint(
    snippet: SnippetCreate, session: AsyncSession = Depends(get_session)
):
    return await create_snippet(session, snippet)

@router.get("/snippets", response_model=list[SnippetResponse])
async def get_all_snippets_endpoint(session: AsyncSession = Depends(get_session)):
    return await get_all_snippet(session)
    