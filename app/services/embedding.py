"""
Step 3 of the pipeline: text -> vector.
Uses fastembed (ONNX-based) instead of sentence-transformers/torch -
same quality embeddings, far lighter on memory, which matters on
Render's free 512MB tier.
"""
from typing import List
from fastembed import TextEmbedding
from app.config import settings

_model = None


def get_model() -> TextEmbedding:
    global _model
    if _model is None:
        _model = TextEmbedding(model_name=settings.EMBEDDING_MODEL)
    return _model


def embed_text(text: str) -> List[float]:
    return list(get_model().embed([text]))[0].tolist()


def embed_batch(texts: List[str]) -> List[List[float]]:
    return [vec.tolist() for vec in get_model().embed(texts)]