"""
LEARN: FastAPI routes for document upload/list/delete.
Each function is a REST endpoint. FastAPI auto-generates:
  - Request validation (via Python type hints)
  - API docs at /docs (Swagger UI — try it in your browser!)
"""
import uuid
import shutil
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.core.config import settings
from app.services.document_processor import process_document, delete_document, list_documents

router = APIRouter(prefix="/documents", tags=["documents"])

ALLOWED_EXTENSIONS = {".pdf", ".txt"}


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    suffix = Path(file.filename).suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, f"Only PDF and TXT files are supported.")

    doc_id = str(uuid.uuid4())
    save_path = Path(settings.upload_dir) / f"{doc_id}{suffix}"

    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    result = process_document(str(save_path), doc_id)
    return {"status": "success", **result}


@router.get("/")
async def get_documents():
    return {"documents": list_documents()}


@router.delete("/{doc_id}")
async def remove_document(doc_id: str):
    success = delete_document(doc_id)
    if not success:
        raise HTTPException(404, "Document not found")
    return {"status": "deleted", "doc_id": doc_id}
