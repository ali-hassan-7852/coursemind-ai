<div align="center">

# CourseMind AI

**AI-powered RAG backend for querying your own course PDFs**

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/pgvector-PostgreSQL-4169E1?logo=postgresql&logoColor=white)
![JWT](https://img.shields.io/badge/Auth-JWT-orange)

</div>

# CourseMind AI

AI-powered Q&A over your own uploaded course textbooks and notes, using Retrieval-Augmented Generation (RAG). Each user's documents and questions are private to their own account.

## Live demo

- **Frontend:** https://coursemind-frontend.vercel.app
- **Backend API docs:** https://coursemaid-ai.onrender.com/docs
- **Frontend repo:** https://github.com/ali-hassan-7852/coursemind-frontend

The backend is on Render's free tier, which spins down after 15 minutes of inactivity - the first request after idle time can take 30-60 seconds to wake up.

## How it works

- Sign up / log in to get a JWT access token
- Upload a PDF - it's split into chunks, embedded, and stored in Postgres (pgvector)
- Ask a question - the system finds the most relevant chunks from your documents and asks an LLM to answer using only that context
- Delete a document any time - it's removed along with all its chunks

## Tech stack

- **FastAPI** - web framework
- **PostgreSQL + pgvector** - stores document chunks and their embeddings in one database (Supabase in production, Docker locally)
- **fastembed** - generates embeddings locally via ONNX Runtime (no API cost, and far lighter on memory than sentence-transformers/torch - chosen specifically to fit free-tier hosting limits)
- **Groq API** (swappable) - generates the final answer
- **JWT + bcrypt** - authentication
- **Render + Vercel + Supabase** - deployment, all on free tiers

## Setup (local development)

### 1. Install dependencies

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Set up PostgreSQL with pgvector

**Recommended: Docker** (pgvector isn't available in the standard Windows PostgreSQL installer, so this avoids building it from source)

```bash
docker run --name coursemind-db -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=coursemind -p 5433:5432 -d pgvector/pgvector:pg16
docker exec -it coursemind-db psql -U postgres -d coursemind -c "CREATE EXTENSION vector;"
```

**Alternative: a hosted database** (what production actually uses) - create a free project at [supabase.com](https://supabase.com), enable the `vector` extension under Database → Extensions, and use its connection string directly.

**Alternative: native PostgreSQL** (if pgvector is already installed on your system, e.g. via Homebrew on macOS or the pgvector package on Linux)

```bash
psql -U postgres -d coursemind -f setup.sql
```

### 3. Configure environment variables

```bash
cp .env.example .env
```

Fill in `.env` with:
- your real `DATABASE_URL` - if using the Docker setup above, this is `postgresql://postgres:postgres@localhost:5433/coursemind`
- a random `JWT_SECRET_KEY` (any long random string)
- `EMBEDDING_MODEL=BAAI/bge-small-en-v1.5`
- an `LLM_API_KEY` (free tier available at console.groq.com)

### 4. Run the server

```bash
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs - this is an interactive page where you can try every endpoint (signup, login, upload, query, delete) directly in the browser, no frontend required.

## API endpoints

| Method | Endpoint                    | Auth required | Description             |
|--------|------------------------------|----------------|--------------------------|
| POST   | `/auth/signup`               | No             | Create an account        |
| POST   | `/auth/login`                | No             | Get a JWT access token   |
| POST   | `/documents/upload`          | Yes            | Upload a PDF             |
| DELETE | `/documents/{document_id}`   | Yes            | Delete a document        |
| POST   | `/query`                     | Yes            | Ask a question           |

To call protected endpoints in `/docs`, click **Authorize**, log in, and every request after that will include your token automatically.

## Project structure

```
app/
├── main.py            # FastAPI app, router registration, CORS config
├── config.py          # all environment variables, in one place
├── database.py        # DB engine/session
├── models.py           # DB tables: User, Document, Chunk
├── schemas.py          # request/response validation
├── dependencies.py     # get_current_user (route protection)
├── routers/            # one file per group of endpoints
│   ├── auth.py
│   ├── upload.py        # upload + delete
│   └── query.py
└── services/            # one file per pipeline step
    ├── pdf_parser.py    # PDF -> text
    ├── chunking.py      # text -> chunks
    ├── embedding.py     # chunks -> vectors (fastembed)
    ├── retrieval.py     # question -> relevant chunks
    ├── llm.py           # chunks + question -> answer (+ markdown cleanup)
    └── auth_service.py  # password hashing + JWT
```

## Running tests

```bash
pytest
```

## Capstone documentation

See `My 10x Solution - Ali Hassan.md` in this repo for the project overview, the 5 implemented concepts, and submission details.

## Possible future improvements

- [ ] Add rate limiting on `/query` if using a paid LLM API
- [ ] `GET /documents` endpoint so uploaded documents persist across sessions in the frontend
- [ ] Automated tests for `/documents/upload` and `/query` (currently only auth is covered)