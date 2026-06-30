from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.retriever import query_rag
from app.services.evaluator import evaluate_rag_response

router = APIRouter(prefix="/query", tags=["query"])


class QueryRequest(BaseModel):
    question: str
    doc_id: str | None = None
    ground_truth: str | None = None  # Optional: user provides the "correct" answer for eval
    run_evaluation: bool = False


class QueryResponse(BaseModel):
    question: str
    answer: str
    sources: list[dict]
    evaluation: dict | None = None


@router.post("/", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    if not request.question.strip():
        raise HTTPException(400, "Question cannot be empty")

    rag_result = query_rag(request.question, request.doc_id)

    evaluation = None
    if request.run_evaluation:
        evaluation = evaluate_rag_response(
            question=request.question,
            answer=rag_result["answer"],
            contexts=rag_result["contexts"],
            ground_truth=request.ground_truth,
        )

    return QueryResponse(
        question=rag_result["question"],
        answer=rag_result["answer"],
        sources=rag_result["sources"],
        evaluation=evaluation,
    )
