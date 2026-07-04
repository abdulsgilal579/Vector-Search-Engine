from fastapi import FastAPI
from .sample_data import SAMPLE_DOCUMENTS
from .search_engine import SemanticSearchEngine

engine = SemanticSearchEngine()
engine.add_document(SAMPLE_DOCUMENTS)

app = FastAPI()

@app.get("/search")
def search(q : str, limit: int = 5):
    return engine.semenaticSearch(q, limit= limit)