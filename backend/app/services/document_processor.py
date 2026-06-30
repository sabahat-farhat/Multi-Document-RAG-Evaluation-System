"""
LEARN: This is the ingestion pipeline — the first half of RAG.
RAG = Retrieval Augmented Generation.
Step 1 (this file): Split docs into chunks → convert to vectors → store in ChromaDB.
Step 2 (retriever.py): On query, convert question to vector → find similar chunks → send to LLM.
"""
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from app.core.config import settings


def get_vectorstore() -> Chroma:
    # LEARN: We use Google's embedding model — it's free and works the same way as OpenAI's.
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004",
        google_api_key=settings.google_api_key,
    )
    return Chroma(
        persist_directory=settings.chroma_persist_dir,
        embedding_function=embeddings,
    )


def process_document(file_path: str, doc_id: str) -> dict:
    path = Path(file_path)

    # LEARN: Loaders read raw files into LangChain Document objects (page_content + metadata)
    if path.suffix.lower() == ".pdf":
        loader = PyPDFLoader(file_path)
    else:
        loader = TextLoader(file_path, encoding="utf-8")

    documents = loader.load()

    # LEARN: We split because LLMs have token limits and because smaller chunks = more precise retrieval.
    # chunk_overlap makes sure sentences that span a boundary aren't cut off.
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )
    chunks = splitter.split_documents(documents)

    for chunk in chunks:
        chunk.metadata["doc_id"] = doc_id
        chunk.metadata["source_file"] = path.name

    # LEARN: Embeddings turn text into a list of numbers (a vector).
    # Semantically similar text → similar vectors → close together in vector space.
    vectorstore = get_vectorstore()
    vectorstore.add_documents(chunks)

    return {
        "doc_id": doc_id,
        "filename": path.name,
        "chunks_created": len(chunks),
        "total_pages": len(documents),
    }


def delete_document(doc_id: str) -> bool:
    vectorstore = get_vectorstore()
    vectorstore._collection.delete(where={"doc_id": doc_id})
    return True


def list_documents() -> list[dict]:
    vectorstore = get_vectorstore()
    results = vectorstore._collection.get(include=["metadatas"])
    seen = {}
    for meta in results["metadatas"]:
        did = meta.get("doc_id")
        if did and did not in seen:
            seen[did] = {
                "doc_id": did,
                "source_file": meta.get("source_file", "unknown"),
            }
    return list(seen.values())
