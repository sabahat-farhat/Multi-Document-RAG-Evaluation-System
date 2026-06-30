from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
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
    search_kwargs = {"k": 4}
    if doc_id:
        search_kwargs["filter"] = {"doc_id": doc_id}

    retriever = vectorstore.as_retriever(search_kwargs=search_kwargs)

    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0,
        api_key=settings.groq_api_key,
    )

    prompt = PromptTemplate.from_template(PROMPT_TEMPLATE)

    # Fetch docs first so we can return them as sources
    source_docs = retriever.invoke(question)
    context_text = "\n\n".join(doc.page_content for doc in source_docs)

    chain = prompt | llm | StrOutputParser()
    answer = chain.invoke({"context": context_text, "question": question})

    sources = [
        {
            "content": doc.page_content[:300],
            "source_file": doc.metadata.get("source_file", ""),
            "page": doc.metadata.get("page", 0),
        }
        for doc in source_docs
    ]

    return {
        "question": question,
        "answer": answer,
        "sources": sources,
        "contexts": [doc.page_content for doc in source_docs],
    }
