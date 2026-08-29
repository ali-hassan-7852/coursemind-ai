"""
POST /documents/upload - upload a PDF, chunk it, embed it, store it.
Requires a valid JWT (get_current_user), so every document is
automatically tied to the logged-in user.
"""
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Document, Chunk, User
from app.schemas import UploadResponse
from app.dependencies import get_current_user
from app.services.pdf_parser import extract_text_from_pdf
from app.services.chunking import chunk_text
from app.services.embedding import embed_batch

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/upload", response_model=UploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    file_bytes = await file.read()
    text = extract_text_from_pdf(file_bytes)

    if not text.strip():
        raise HTTPException(status_code=400, detail="Could not extract any text from this PDF")

    text_chunks = chunk_text(text)
    embeddings = embed_batch(text_chunks)

    document = Document(filename=file.filename, user_id=current_user.id)
    db.add(document)
    db.flush()  # assigns document.id before we commit, so chunks can reference it

    for content, embedding in zip(text_chunks, embeddings):
        db.add(Chunk(
            document_id=document.id,
            user_id=current_user.id,
            content=content,
            embedding=embedding,
        ))

    db.commit()

    return UploadResponse(
        document_id=document.id,
        filename=document.filename,
        chunks_created=len(text_chunks),
    )
