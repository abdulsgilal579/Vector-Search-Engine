# Vector Search Engine

A tutorial-friendly Retrieval-Augmented Generation (RAG) system built from scratch. Ingest PDFs, store their meaning as vectors in Qdrant, and ask natural-language questions answered by an LLM grounded in your documents.

## What's inside

- **Semantic search** over a small in-memory document set (from the first tutorial).
- **Persistent vector store** backed by Qdrant.
- **PDF ingestion pipeline**: extract → chunk → embed → upsert.
- **RAG endpoint** that retrieves relevant chunks and asks Groq's LLM for a grounded answer.
- **FastAPI** interface with auto-generated Swagger docs.

## Architecture

```
PDF file
   │
   ▼
load_pdf ──► chunk_text ──► Embedding ──► QdrantStore.addDocument
                                                  │
                                                  ▼
                                             Qdrant DB
                                                  ▲
                                                  │
User question ──► Embedding ──► QdrantStore.search ──► top-K chunks
                                                             │
                                                             ▼
                                                        Groq LLM
                                                             │
                                                             ▼
                                                        Answer + sources
```

## Tech stack

| Component | Choice |
|---|---|
| Embedding model | `sentence-transformers/all-MiniLM-L6-v2` (384-dim) |
| Vector database | Qdrant (Docker) |
| PDF extraction | `pypdf` |
| LLM | Groq (`llama-3.3-70b-versatile`) |
| API | FastAPI + Uvicorn |

## Setup

### 1. Clone and create a virtual environment
```bash
git clone <this-repo>
cd Vector-Search-Engine
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Start Qdrant (Docker)
```bash
docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
```
Dashboard: [http://localhost:6333/dashboard](http://localhost:6333/dashboard)

### 4. Configure environment
Create a `.env` file in the project root:
```
GROQ_API_KEY=gsk_your_key_here
```
Get a free key at [console.groq.com](https://console.groq.com/keys).

### 5. Run the API
```bash
uvicorn vector-search-engine.main:app --reload
```
Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

## API endpoints

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/search` | Semantic search over sample in-memory documents |
| `POST` | `/ingest?pdf_path=...` | Extract, chunk, embed, and store a PDF in Qdrant |
| `GET` | `/pdf-search?q=...` | Nearest-neighbor chunks from ingested PDFs |
| `GET` | `/ask?q=...` | Full RAG: retrieve top-K chunks and answer via LLM |

### Example
```bash
# Ingest a PDF
curl -X POST "http://localhost:8000/ingest?pdf_path=/full/path/to/file.pdf"

# Ask a question
curl "http://localhost:8000/ask?q=Who did I email about the research opportunity"
```

## Project structure

```
vector-search-engine/
├── embeddings.py           # SentenceTransformer wrapper
├── search_engine.py        # In-memory semantic search (tutorial 1)
├── vector_stroe_qdrant.py  # QdrantStore: connect, create, upsert, search
├── pdf_loader.py           # PDF text extraction and chunking
├── ingest.py               # PDF → chunks → vectors → Qdrant
├── llm.py                  # Groq LLM wrapper (RAG prompt)
├── main.py                 # FastAPI app and routes
└── sample_data.py          # Toy dataset for /search
```

## How the RAG loop works

1. **Ingest**: PDF is loaded, split into overlapping word-chunks, embedded, and upserted into the `pdfs` collection.
2. **Query**: user's question is embedded with the same model.
3. **Retrieve**: Qdrant returns the top-K most similar chunks by cosine similarity.
4. **Generate**: the chunks are stitched into a context block and sent to Groq with a strict "answer only from context" prompt.
5. **Respond**: JSON returns the answer alongside source chunks (page number + preview) for traceability.

## Tutorial playlist

Follow along on YouTube: [Full playlist](https://www.youtube.com/watch?v=ZafO108joIc&list=PLbcQSpAqoCCU)
