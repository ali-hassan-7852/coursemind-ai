"""
Step 4 of the pipeline: given a question, find the most relevant chunks
- filtered to the current user's own documents only.
"""
from typing import List
from sqlalchemy.orm import Session
from app.models import Chunk
from app.services.embedding import embed_text


def retrieve_relevant_chunks(
    db: Session, question: str, user_id: int, top_k: int = 4
) -> List[Chunk]:
    question_embedding = embed_text(question)

    return (
        db.query(Chunk)
        .filter(Chunk.user_id == user_id)
        .order_by(Chunk.embedding.cosine_distance(question_embedding))
        .limit(top_k)
        .all()
    )
