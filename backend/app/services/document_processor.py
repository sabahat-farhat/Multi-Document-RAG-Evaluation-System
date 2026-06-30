from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from app.core.config import settings

# Runs locally — no API key needed. Downloads once (~90MB), then cached.
_embeddings = None

def get_embeddings():
    global _embeddings
    if _embeddings is None:
        _embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"},
        )
    return _embeddings

def get_vectorstore() -> Chroma:
    return Chroma(
        persist_directory=settings.chroma_persist_dir,
        embedding_function=get_embeddings(),
    )

def process_document(file_path: str, doc_id: str) -> dict:
    path = Path(file_path)
    if path.suffix.lower() == ".pdf":
        loader = PyPDFLoader(file_path)
    else:
        loader = TextLoader(file_path, encoding="utf-8")

    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )
    chunks = splitter.split_documents(documents)

    for chunk in chunks:
        chunk.metadata["doc_id"] = doc_id
        chunk.metadata["source_file"] = path.name

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
            seen[did] = {"doc_id": did, "source_file": meta.get("source_file", "unknown")}
    return list(seen.values())
