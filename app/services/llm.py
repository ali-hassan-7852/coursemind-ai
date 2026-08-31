"""
Step 5 of the pipeline: send the question + retrieved chunks to an LLM
and get back a grounded answer.

Uses Groq's free-tier API by default (OpenAI-compatible format) - swap
the URL/model in .env to use OpenAI, Together, or any compatible provider.
"""
from typing import List
import requests
from app.config import settings

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


def generate_answer(question: str, context_chunks: List[str]) -> str:
    context = "\n\n".join(context_chunks)

    prompt = (
    "Answer the question using only the context below. "
    "If the answer isn't in the context, say you don't have enough information.\n\n"
    "Formatting rules: write in standard Markdown. For bold text always use "
    "matching double asterisks like **this** - never a single asterisk, and "
    "never mismatch the number of asterisks on each side. Prefer short "
    "paragraphs and simple bullet points over tables; only use a table if "
    "the answer is genuinely tabular data.\n\n"
    f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
    )

    response = requests.post(
        GROQ_URL,
        headers={"Authorization": f"Bearer {settings.LLM_API_KEY}"},
        json={
            "model": settings.LLM_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2,
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"]
