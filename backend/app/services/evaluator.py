from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from datasets import Dataset
from langchain_groq import ChatGroq
from app.core.config import settings
from app.services.document_processor import get_embeddings


def evaluate_rag_response(
    question: str,
    answer: str,
    contexts: list[str],
    ground_truth: str | None = None,
) -> dict:
    data = {
        "question": [question],
        "answer": [answer],
        "contexts": [contexts],
        "ground_truth": [ground_truth or ""],
    }
    dataset = Dataset.from_dict(data)

    llm = LangchainLLMWrapper(ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0,
        api_key=settings.groq_api_key,
    ))
    embeddings = LangchainEmbeddingsWrapper(get_embeddings())

    result = evaluate(
        dataset=dataset,
        metrics=[faithfulness, answer_relevancy],
        llm=llm,
        embeddings=embeddings,
    )

    scores = result.to_pandas().iloc[0].to_dict()
    return {
        "faithfulness": round(float(scores.get("faithfulness", 0)), 3),
        "answer_relevancy": round(float(scores.get("answer_relevancy", 0)), 3),
        "context_precision": None,
    }
