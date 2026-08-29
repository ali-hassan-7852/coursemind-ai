"""
POST /query - ask a natural-language question.
Only ever searches the logged-in user's own uploaded documents.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import QueryRequest, QueryResponse, SourceChunk
from app.dependencies import get_current_user
from app.services.retrieval import retrieve_relevant_chunks
from app.services.llm import generate_answer

router = APIRouter(prefix="/query", tags=["query"])


@router.post("", response_model=QueryResponse)
def ask_question(
    request: QueryRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    relevant_chunks = retrieve_relevant_chunks(db, request.question, current_user.id)

    if not relevant_chunks:
        return QueryResponse(
            answer="You haven't uploaded any documents yet, or nothing relevant was found.",
            sources=[],
        )

    context_texts = [chunk.content for chunk in relevant_chunks]
    answer = generate_answer(request.question, context_texts)

    sources = [
        SourceChunk(content=chunk.content[:200], document_filename=chunk.document.filename)
        for chunk in relevant_chunks
    ]

    return QueryResponse(answer=answer, sources=sources)
