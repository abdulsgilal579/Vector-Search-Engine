from fastapi import FastAPI

from vector_store import VectorStore
from embeddings import Embedding
from ingest import ingest
from llm import ask_llm

app = FastAPI()

store = VectorStore(collection_name="Donal Trump")
embedder = Embedding()

@app.post("/ingest")
def ingest_pdf(file_path):
    count = ingest(pdf_path=file_path, store=store, embedding=embedder)
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