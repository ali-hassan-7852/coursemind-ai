"""
Pydantic models = the shape of data going in/out of the API.
Kept separate from models.py (the DB shape) on purpose - the two
don't always need to match.
"""
from pydantic import BaseModel, EmailStr
from typing import List


# --- Auth ---

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# --- Documents ---

class UploadResponse(BaseModel):
    document_id: int
    filename: str
    chunks_created: int


# --- Query ---

class QueryRequest(BaseModel):
    question: str


class SourceChunk(BaseModel):
    content: str
    document_filename: str


class QueryResponse(BaseModel):
    answer: str
    sources: List[SourceChunk]
