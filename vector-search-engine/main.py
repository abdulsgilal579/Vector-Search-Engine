from fastapi import FastAPI

from .sample_data import SAMPLE_DOCUMENTS
from .search_engine import SemanticSearchEngine
from .vector_stroe_qdrant import QdrantStore
from .embeddings import Embedding
from .ingest import ingest_pdf

from .llm import ask_llm

engine = SemanticSearchEngine()
embedder = Embedding()
store = QdrantStore(collection_name="pdfs")

engine.add_document(SAMPLE_DOCUMENTS)

app = FastAPI()

@app.get("/search")
def search(q: str, limit: int = 5):
    return engine.semantic_search(q, limit=limit)


@app.post("/ingest")
def ingest(pdf_path: str):
    count = ingest_pdf(pdf_path, store, embedder)
    return {"status": "ok", "chunks_ingested": count, "source": pdf_path}


@app.get("/pdf-search")
def pdf_search(q: str, limit: int = 5):
    query_vector = embedder.encode([q])[0]
    return store.search(query_vector, k=limit)

@app.get("/ask")
def ask(q: str, k: int = 5):
    query_vector = embedder.encode([q])[0]
    matches = store.search(query_vector, k=k)
    context = "\n\n".join([m["text"] for m in matches])
    answer = ask_llm(q, context)
    return {
        "question": q,
        "answer": answer,
        "sources": [
            {"page": m["page"], "score": m["score"], "preview": m["text"][:200]}
            for m in matches
        ],
    }
