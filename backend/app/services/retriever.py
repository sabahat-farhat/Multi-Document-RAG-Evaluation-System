"""
LEARN: This is the retrieval + generation half of RAG.
When a user asks a question:
  1. We embed the question (same model as we used for chunks).
  2. ChromaDB finds the top-K most similar chunks.
  3. We stuff those chunks as "context" into a prompt.
  4. GPT reads the context and answers — it can only use what we gave it.
That last point is the key insight: the LLM isn't "remembering" your docs,
it's reading the relevant excerpt fresh every time.
"""
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from app.core.config import settings
from app.services.document_processor import get_vectorstore


PROMPT_TEMPLATE = """You are a helpful assistant. Use ONLY the context below to answer.
If the answer is not in the context, say "I don't have enough information to answer that."

Context:
{context}

Question: {question}

Answer:"""


def query_rag(question: str, doc_id: str | None = None) -> dict:
    vectorstore = get_vectorstore()

    # LEARN: If doc_id is given, we filter the vector search to only chunks from that document.
    search_kwargs = {"k": settings.top_k_results}
    if doc_id:
        search_kwargs["filter"] = {"doc_id": doc_id}

    retriever = vectorstore.as_retriever(search_kwargs=search_kwargs)

    # LEARN: RetrievalQA is a LangChain "chain" — it wires retriever + LLM automatically.
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0,
        google_api_key=settings.google_api_key,
    )

    prompt = PromptTemplate(
        template=PROMPT_TEMPLATE,
        input_variables=["context", "question"],
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",  # "stuff" = put all chunks into one prompt
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt},
    )

    result = qa_chain.invoke({"query": question})

    sources = []
    for doc in result["source_documents"]:
        sources.append({
            "content": doc.page_content[:300],
            "source_file": doc.metadata.get("source_file", ""),
            "page": doc.metadata.get("page", 0),
        })

    return {
        "question": question,
        "answer": result["result"],
        "sources": sources,
        "contexts": [doc.page_content for doc in result["source_documents"]],
    }
