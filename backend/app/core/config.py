from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    google_api_key: str
    chroma_persist_dir: str = "./chroma_db"
    upload_dir: str = "../data/uploads"
    chunk_size: int = 500
    chunk_overlap: int = 50
    top_k_results: int = 4

    class Config:
        env_file = ".env"


settings = Settings()

Path(settings.upload_dir).mkdir(parents=True, exist_ok=True)
Path(settings.chroma_persist_dir).mkdir(parents=True, exist_ok=True)
