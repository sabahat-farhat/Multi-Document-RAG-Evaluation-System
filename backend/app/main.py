"""
LEARN: main.py is the entry point of the FastAPI app.
FastAPI is similar to Flask but much faster and auto-generates API docs.
CORS middleware lets the React frontend (on port 5173) talk to this backend (port 8000).
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import documents, query

app = FastAPI(
    title="RAG Evaluation System",
    description="Multi-document RAG with RAGAS evaluation dashboard",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documents.router)
app.include_router(query.router)


@app.get("/health")
async def health():
    return {"status": "ok"}
