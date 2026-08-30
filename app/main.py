"""
App entrypoint. Run with:
    uvicorn app.main:app --reload
Then open http://127.0.0.1:8000/docs to try every endpoint in the browser.
"""
from fastapi import FastAPI
from app.database import Base, engine
from app.routers import auth, upload, query
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CourseMind AI",
    description="AI-powered Q&A over your own uploaded course documents.",
    version="1.0.0",
)



app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://coursemind-frontend-4my1t57zi-ali-s-projects-ccc9.vercel.app/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(upload.router)
app.include_router(query.router)


@app.get("/")
def root():
    return {"message": "CourseMind AI is running. Visit /docs to try it out."}
