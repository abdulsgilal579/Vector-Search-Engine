from .embeddings import Embedding
import numpy as np

class SemanticSearchEngine:
    def __init__(self):
        self.embedder = Embedding()
        self.text = []
        self.vector = []
    
    def add_document(self, text):
        vectors = self.embedder.encode(text)
        self.text.extend(text)
        self.vector.extend(vectors)
    
    def semenaticSearch(self, query, limit = 5):
        query_vector = self.embedder.encode([query])[0]
        score = np.dot(self.vector, query_vector)
        top_results = np.argsort(score)[::-1][:limit]
        return[
            {"Text": self.text[i], "Score": round(float(score[i]), 4)}
            for i in top_results
        ]
        


    




