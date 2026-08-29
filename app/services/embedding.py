"""
Step 3 of the pipeline: text -> vector.
Model loads once and is reused (loading it per-request would be slow).
"""
from typing import List
from sentence_transformers import SentenceTransformer
from app.config import settings

_model = None


def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(settings.EMBEDDING_MODEL)
    return _model


def embed_text(text: str) -> List[float]:
    return get_model().encode(text).tolist()


def embed_batch(texts: List[str]) -> List[List[float]]:
    return get_model().encode(texts).tolist()
