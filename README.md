# Multi-Document RAG Evaluation System

Upload PDFs/text files, ask questions, get answers grounded in your documents, and see RAGAS quality scores.

## Stack
- **Backend**: FastAPI + LangChain + ChromaDB + RAGAS
- **Frontend**: React + Vite + Tailwind CSS + Recharts

## Setup

### 1. Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env
# Then open .env and paste your OpenAI API key

# Run the server
uvicorn app.main:app --reload
```

Backend runs at: http://localhost:8000
API docs (Swagger UI): http://localhost:8000/docs

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at: http://localhost:5173

## How it works

```
PDF/TXT → chunk (500 tokens) → embed → ChromaDB
                                              ↓
Question → embed → similarity search → top 4 chunks → GPT-4o-mini → Answer
                                                                         ↓
                                                              RAGAS evaluation
                                                    (faithfulness, relevancy, precision)
```

## RAGAS Scores
| Metric | What it measures | Range |
|--------|-----------------|-------|
| Faithfulness | Is the answer supported by the context? | 0–1 |
| Answer Relevancy | Does the answer address the question? | 0–1 |
| Context Precision | Did retrieval fetch the right chunks? (needs ground truth) | 0–1 |
