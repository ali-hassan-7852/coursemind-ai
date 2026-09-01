# My 10x Solution - Ali Hassan

## 1. The problem

Students preparing for exams or assignments need specific answers buried inside dense textbooks, lecture notes, and PDFs. Keyword search (Ctrl+F) only matches exact wording, so a student asking "why does recursion need a base case" gets nothing useful from a textbook that explains the same idea in different words. Finding the right passage in a 100-page PDF can take longer than actually understanding the concept once you find it. This wastes study time and makes self-directed learning harder than it should be.

**CourseMind AI** solves this: a student uploads their own course PDFs once, then asks questions in plain English and gets an answer grounded in their own material - with the exact passage it came from, so they can verify it themselves. It's the difference between searching a book and asking someone who's actually read it.

## 2. How it works

CourseMind AI is a full RAG (Retrieval-Augmented Generation) system with a Python/FastAPI backend and a React frontend, deployed as a live, working product.

**The pipeline:**
1. A student uploads a PDF through the web app
2. The backend extracts the text and splits it into overlapping chunks
3. Each chunk is converted into a vector embedding (using `fastembed`, a lightweight ONNX-based library chosen specifically to fit within free-tier hosting memory limits)
4. Chunks and their embeddings are stored together in PostgreSQL, using the `pgvector` extension
5. When the student asks a question, it's embedded the same way, and the database finds the most semantically similar chunks via cosine similarity
6. Those chunks plus the question are sent to an LLM (Groq), which generates an answer grounded only in that retrieved context
7. The answer is returned along with the exact source passage it came from

Every document and every answer is scoped to the logged-in user via JWT authentication - one student's uploads are never visible to another.

**Tech stack:** FastAPI, PostgreSQL + pgvector (Supabase), fastembed, Groq LLM API, JWT auth with bcrypt password hashing, React + Vite + Tailwind CSS on the frontend.

**Live and deployed:** backend on Render, frontend on Vercel, database on Supabase - all on free tiers, all reachable by URL right now.

## 3. The 5 concepts implemented

| # | Concept | Table | Where it lives |
|---|---------|-------|-----------------|
| 1 | API endpoints | Main | FastAPI routers (`app/routers/`) - proper status codes (200/400/401/404), Pydantic request/response validation |
| 2 | Database | Main | PostgreSQL + pgvector via Supabase (`app/models.py`, `app/database.py`) - persists across restarts |
| 3 | Authentication | Main | JWT-based auth (`app/services/auth_service.py`, `app/dependencies.py`) - protected routes, verified per-user data isolation |
| 4 | RAG with citations | **Swap** | The full `/query` pipeline (`app/services/retrieval.py`, `app/services/llm.py`) - answers grounded in the user's own documents, with sources returned alongside every answer |
| 5 | Deployment | **Swap** | Live on Render (API) + Vercel (frontend) + Supabase (database) - a real URL, not a local demo |

**Why these two swaps:**
- **RAG with citations** was swapped in instead of forcing something like background jobs or a caching layer, because grounded, sourced retrieval is the actual technical core of this project - not an add-on, but the entire point.
- **Deployment** was swapped in instead of building a PDF/email reporting feature that wouldn't naturally fit a real-time Q&A tool - shipping the system live, on a real URL, mattered more for making this genuinely usable and demo-able.

## 4. How to run it

**Try it live (no setup required):**
Visit the deployed frontend, sign up, upload a PDF, and ask a question:
`https://coursemind-frontend.vercel.app`

**To run it locally for development:**
1. Clone both repos (`coursemind-ai-backend` and `coursemind-frontend`)
2. Backend: `pip install -r requirements.txt`, set up a `.env` from `.env.example`, run `uvicorn app.main:app --reload`
3. Frontend: `npm install`, set `VITE_API_BASE_URL` in `.env`, run `npm run dev`
4. Full setup details are in each repo's README

## 5. Repositories

- Backend: https://github.com/ali-hassan-7852/coursemind-ai
- Frontend: https://github.com/ali-hassan-7852/coursemind-frontend
