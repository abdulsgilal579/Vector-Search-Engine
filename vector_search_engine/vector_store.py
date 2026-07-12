from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from uuid import uuid4

class VectorStore:
    def __init__(self, collection_name, url="http://localhost:6333", vector_size = 384, distance = Distance.COSINE):
        self.qdrant_client = QdrantClient(url=url)
        self.collection_name = collection_name
        self.vector_size = vector_size
        self.distance = distance
        self.ensureCollection()
    
    def ensureCollection(self):
        if not self.qdrant_client.collection_exists(self.collection_name):
            self.qdrant_client.create_collection(
                collection_name= self.collection_name,
                vectors_config= VectorParams(size = self.vector_size, distance= self.distance)
            )
        else:
            pass
    
    def addDocument(self, texts, vectors, metadatas):
        points = []
        for text, vector, metadata in zip(texts, vectors, metadatas):
            point = PointStruct(
                id = uuid4().hex,
                vector = vector,
                payload = {"text": text, **metadata}
            )
            points.append(point)
        self.qdrant_client.upsert(
            collection_name= self.collection_name,
            points = points
        )
    
    def search(self, query_vector, k=5):
        result = self.qdrant_client.query_points(
            collection_name = self.collection_name,
            query = query_vector,
            limit= k,
            with_payload= True
        )
        return result.points


obj = VectorStore(collection_name="fahad")
