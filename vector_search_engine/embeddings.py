from sentence_transformers import SentenceTransformer

class Embedding:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
    
    def encode(self, text):
        vector = self.model.encode(
            text,
            normalize_embeddings = True,
            show_progress_bar= False
        )
        return [v.tolist() for v in vector]