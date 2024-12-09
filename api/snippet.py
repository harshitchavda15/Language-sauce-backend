from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .crud.snippet import create_snippet,get_all_snippet
from .schemas.snippet import SnippetCreate,Snippet
from .database import get_session

router=APIRouter()

@router.post("/snippets",response_model=Snippet)
async def create_snippet_endpoint(snippet: SnippetCreate,session: AsyncSession = Depends(get_session)):
    return await create_snippet(session, snippet.dict())

@router.get("/snippets",response_model=List[Snippet])
async def get_all_snippets(session: AsyncSession = Depends(get_session)):
    snippets= get_all_snippet(session)
    return snippets

