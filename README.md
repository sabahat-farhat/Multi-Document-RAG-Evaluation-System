# Multi-Document RAG Evaluation System

Upload PDFs/text files, ask questions, get answers grounded in your documents, and see RAGAS quality scores.

## Stack
- **Backend**: FastAPI + LangChain + ChromaDB + RAGAS
- **LLM**: Groq (free) — llama-3.1-8b-instant
- **Embeddings**: sentence-transformers all-MiniLM-L6-v2 (local, no API key needed)
- **Frontend**: React + Vite + Tailwind CSS + Recharts

## Setup

### 1. Get a free Groq API key
- Go to **console.groq.com**
- Sign up with Google or email (free, no credit card)
- Go to API Keys → Create API key
- Copy the key

### 2. Backend

```bash
cd backend

# Create virtual environment with Python 3.11
py -3.11 -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env
# Open .env and paste your Groq API key

# Run the server
uvicorn app.main:app --reload
```

Backend runs at: http://localhost:8000
API docs (Swagger UI): http://localhost:8000/docs

> **Note:** First startup downloads the embedding model (~90MB). This takes about 1 minute once, then it's cached forever.

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at: http://localhost:5173

## .env file format

```
GROQ_API_KEY=your_groq_key_here
CHROMA_PERSIST_DIR=./chroma_db
UPLOAD_DIR=../data/uploads
```

## How it works

```
PDF/TXT → chunk (500 tokens) → embed (local model) → ChromaDB
                                                            ↓
Question → embed → similarity search → top 4 chunks → Groq LLaMA → Answer
                                                                        ↓
                                                           RAGAS evaluation
                                                 (faithfulness, answer relevancy)
```

## RAGAS Scores
| Metric | What it measures | Range |
|--------|-----------------|-------|
| Faithfulness | Is the answer supported by the retrieved context? Catches hallucinations. | 0–1 |
| Answer Relevancy | Does the answer actually address the question asked? | 0–1 |

## Why these choices?
- **Groq** is free with a generous daily limit and extremely fast (hundreds of tokens/sec)
- **Local embeddings** mean zero API cost for document ingestion — you can upload as many files as you want
- **LLaMA 3.1 8B** is a strong open-source model that performs well for RAG tasks
