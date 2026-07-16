from fastapi import FastAPI

from vector_search_engine.vector_store import VectorStore
from vector_search_engine.embeddings import Embedding
from vector_search_engine.ingest import ingest
from vector_search_engine.llm import ask_llm

app = FastAPI()

store = VectorStore(collection_name="Donal Trump")
embedder = Embedding()

@app.post("/ingest")
def ingest_pdf(file_path):
    count = ingest(pdf_path=file_path, store=store, embedder=embedder)
    return {"Response:": "Ok", "Count: ": count, "Source": file_path}

@app.get("/pdf_search")
def pdf_search_vector(q: str, k:int = 5):
    query_vector = embedder.encode([q])[0]
    return store.search(query_vector=query_vector, k=k)

@app.get("/ask")
def ask_llm_grok(q: str, limit: int = 5):
    query_vector = embedder.encode([q])[0]
    matches = store.search(query_vector = query_vector, k=limit)
    context = "\n\n".join([m.payload["text"] for m in matches])
    llm_response = ask_llm(question=q, context=context)
    return {
        "Response:": "OK",
        "Lmm Result: ": llm_response
    }