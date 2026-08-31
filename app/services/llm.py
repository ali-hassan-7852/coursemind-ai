# """
# Step 5 of the pipeline: send the question + retrieved chunks to an LLM
# and get back a grounded answer.

# Uses Groq's free-tier API by default (OpenAI-compatible format) - swap
# the URL/model in .env to use OpenAI, Together, or any compatible provider.
# """
# from typing import List
# import requests
# from app.config import settings

# GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


# def generate_answer(question: str, context_chunks: List[str]) -> str:
#     context = "\n\n".join(context_chunks)

#     prompt = (
#     "Answer the question using only the context below, in plain "
#     "conversational sentences - like you're explaining it out loud to a "
#     "student. Do not use any Markdown formatting: no **bold**, no bullet "
#     "points, no numbered lists, no headings, no tables. Just write it as "
#     "normal flowing paragraphs. If the answer isn't in the context, say "
#     "you don't have enough information.\n\n"
#     f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
#     )

#     response = requests.post(
#         GROQ_URL,
#         headers={"Authorization": f"Bearer {settings.LLM_API_KEY}"},
#         json={
#             "model": settings.LLM_MODEL,
#             "messages": [{"role": "user", "content": prompt}],
#             "temperature": 0.2,
#         },
#         timeout=30,
#     )
#     response.raise_for_status()
#     data = response.json()
#     return data["choices"][0]["message"]["content"]

"""
Step 5 of the pipeline: send the question + retrieved chunks to an LLM
and get back a grounded answer.

Uses Groq's free-tier API by default (OpenAI-compatible format) - swap
the URL/model in .env to use OpenAI, Together, or any compatible provider.
"""
import re
from typing import List
import requests
from app.config import settings

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


def clean_markdown(text: str) -> str:
    """
    Strip Markdown syntax so answers read as plain prose, no matter what
    the model actually outputs. Prompt instructions alone are only a
    suggestion the model can ignore - this guarantees clean text every time.
    """
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)          # **bold**
    text = re.sub(r"\*(.*?)\*", r"\1", text)                # *italic*
    text = re.sub(r"__(.*?)__", r"\1", text)                # __bold__
    text = re.sub(r"(?<!\w)_(.*?)_(?!\w)", r"\1", text)     # _italic_
    text = re.sub(r"^#{1,6}\s*", "", text, flags=re.MULTILINE)      # # headings
    text = re.sub(r"^\s*[-*+]\s+", "", text, flags=re.MULTILINE)    # - bullet lists
    text = re.sub(r"^\s*\d+\.\s+", "", text, flags=re.MULTILINE)    # 1. numbered lists
    text = re.sub(r"^\s*\|?[-:\s|]+\|?\s*$", "", text, flags=re.MULTILINE)  # table separators
    text = text.replace("|", " ")                            # table pipes
    text = re.sub(r"```[a-zA-Z]*\n?", "", text)             # code fences
    text = text.replace("`", "")                             # inline code ticks
    text = text.replace("*", "")                             # any stray leftover asterisks
    text = re.sub(r"\s*\n+\s*", " ", text)                  # collapse line breaks into prose
    text = re.sub(r"\s{2,}", " ", text)
    return text.strip()


def generate_answer(question: str, context_chunks: List[str]) -> str:
    context = "\n\n".join(context_chunks)

    prompt = (
        "Answer the question using only the context below, in plain "
        "conversational sentences - like you're explaining it out loud to a "
        "student. Do not use any Markdown formatting: no **bold**, no bullet "
        "points, no numbered lists, no headings, no tables. Just write it as "
        "normal flowing paragraphs. If the answer isn't in the context, say "
        "you don't have enough information.\n\n"
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
    raw_answer = data["choices"][0]["message"]["content"]
    return clean_markdown(raw_answer)