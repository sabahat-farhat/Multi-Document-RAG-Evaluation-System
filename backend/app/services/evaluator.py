"""
LEARN: This is the RAGAS evaluation layer — what makes this project stand out.
RAGAS scores 3 things about a RAG system's answer:

  faithfulness   — Is the answer factually grounded in the retrieved context?
                   (Catches hallucinations: model making up things not in your docs)

  answer_relevancy — Does the answer actually address the question asked?
                     (Catches vague/off-topic responses)

  context_precision — Did retrieval fetch the RIGHT chunks?
                      (Catches retrieval quality issues — garbage in, garbage out)

Each score is 0.0 → 1.0. Higher is better.
"""
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision
from datasets import Dataset
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from app.core.config import settings


def evaluate_rag_response(
    question: str,
    answer: str,
    contexts: list[str],
    ground_truth: str | None = None,
) -> dict:
    # RAGAS needs data in a HuggingFace Dataset format
    data = {
        "question": [question],
        "answer": [answer],
        "contexts": [contexts],
        "ground_truth": [ground_truth or ""],
    }
    dataset = Dataset.from_dict(data)

    metrics = [faithfulness, answer_relevancy]
    if ground_truth:
        metrics.append(context_precision)

    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=settings.google_api_key)
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004",
        google_api_key=settings.google_api_key,
    )

    # LEARN: RAGAS uses GPT itself to judge the quality of the RAG output.
    # This is called "LLM-as-a-judge" — a common pattern in production eval pipelines.
    result = evaluate(
        dataset=dataset,
        metrics=metrics,
        llm=llm,
        embeddings=embeddings,
    )

    scores = result.to_pandas().iloc[0].to_dict()

    return {
        "faithfulness": round(float(scores.get("faithfulness", 0)), 3),
        "answer_relevancy": round(float(scores.get("answer_relevancy", 0)), 3),
        "context_precision": round(float(scores.get("context_precision", 0)), 3) if ground_truth else None,
    }
